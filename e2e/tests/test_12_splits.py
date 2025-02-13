# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 The HuggingFace Authors.

import pytest

from .utils import get, get_openapi_body_example, poll, poll_splits, post_refresh


@pytest.mark.parametrize(
    "status,name,dataset,config,error_code",
    [
        #  (200, "all splits in a dataset", "ibm/duorc", None, None),
        #  (200, "splits for a single config", "emotion", "unsplit", None)
        (
            401,
            "inexistent dataset, and not authenticated",
            "severo/inexistent-dataset",
            None,
            "ExternalUnauthenticatedError",
        ),
        # (
        #     401,
        #     "gated-dataset",
        #     "severo/dummy_gated", None,
        #     "ExternalUnauthenticatedError",
        # ),
        # (
        #     401,
        #     "private-dataset",
        #     "severo/dummy_private", None,
        #     "ExternalUnauthenticatedError",
        # ),
        (422, "missing dataset parameter", "", None, "MissingRequiredParameter"),
        (422, "empty dataset parameter", None, None, "MissingRequiredParameter"),
        # (500, "SplitsNotFoundError", "natural_questions", None, "SplitsNamesError"),
        # (500, "FileNotFoundError", "akhaliq/test", None, "SplitsNamesError"),
        # (500, "not-ready", "severo/fix-401", None, "SplitsResponseNotReady"),
        # not tested: 'internal_error'
    ],
)
def test_splits_using_openapi(status: int, name: str, dataset: str, config: str, error_code: str) -> None:
    body = get_openapi_body_example("/splits", status, name)
    config_query = f"&config={config}" if config else ""

    if name == "empty dataset parameter":
        r_splits = poll("/splits?dataset=", error_field="error")
    elif name == "missing dataset parameter":
        r_splits = poll("/splits", error_field="error")
    else:
        post_refresh(dataset)
        # poll the endpoint before the worker had the chance to process it
        r_splits = (
            get(f"/splits?dataset={dataset}{config_query}") if name == "not-ready" else poll_splits(dataset, config)
        )

    assert r_splits.status_code == status, f"{r_splits.status_code} - {r_splits.text}"
    assert r_splits.json() == body, r_splits.text
    if error_code is not None:
        assert r_splits.headers["X-Error-Code"] == error_code, r_splits.headers["X-Error-Code"]
    else:
        assert "X-Error-Code" not in r_splits.headers, r_splits.headers["X-Error-Code"]


@pytest.mark.parametrize(
    "status,dataset,config,error_code",
    [
        # (200, "ibm/duorc", "SelfRC", None),
        (401, "missing-parameter", None, "ExternalUnauthenticatedError")
        # missing config will result in asking dataset but it does not exist
    ],
)
def test_splits_with_config_using_openapi(status: int, dataset: str, config: str, error_code: str) -> None:
    r_splits = (
        poll(f"/splits?dataset={dataset}&config=", error_field="error")
        if error_code
        else poll(f"/splits?dataset={dataset}&config={config}")
    )

    assert r_splits.status_code == status, f"{r_splits.status_code} - {r_splits.text}"

    if error_code is None:
        assert all(split["config"] == config for split in r_splits.json()["splits"])
        # all splits must belong to the provided config

        assert "X-Error-Code" not in r_splits.headers, r_splits.headers["X-Error-Code"]
    else:
        assert r_splits.headers["X-Error-Code"] == error_code, r_splits.headers["X-Error-Code"]
