# Check dataset validity

Before you download a dataset from the Hub, it is helpful to know if a specific dataset you're interested in is available. Datasets Server provides the `/is-valid` endpoint to check if a specific dataset works without any errors.

The API endpoint will return an error for datasets that cannot be loaded with the [🤗 Datasets](https://github.com/huggingface/datasets) library, for example, because the data hasn't been uploaded or the format is not supported.

<Tip warning={true}>
  The largest datasets are partially supported by Datasets Server. If they are{" "}
  <a href="https://huggingface.co/docs/datasets/stream">streamable</a>, Datasets
  Server can extract the first 100 rows without downloading the whole dataset.
  This is especially useful for previewing large datasets where downloading the
  whole dataset may take hours! See the <code>preview</code> field in the
  response of <code>/is-valid</code> to check if a dataset is partially
  supported.
</Tip>

This guide shows you how to check dataset validity programmatically, but free to try it out with [Postman](https://www.postman.com/huggingface/workspace/hugging-face-apis/request/23242779-17b761d0-b2b8-4638-a4f7-73be9049c324), [RapidAPI](https://rapidapi.com/hugging-face-hugging-face-default/api/hugging-face-datasets-api), or [ReDoc](https://redocly.github.io/redoc/?url=https://datasets-server.huggingface.co/openapi.json#operation/isValidDataset).

## Check if a dataset is valid

`/is-valid` checks whether a specific dataset loads without any error. This endpoint's query parameter requires you to specify the name of the dataset:

<inferencesnippet>
<python>
```python
import requests
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://datasets-server.huggingface.co/is-valid?dataset=rotten_tomatoes"
def query():
    response = requests.get(API_URL, headers=headers)
    return response.json()
data = query()
```
</python>
<js>
```js
import fetch from "node-fetch";
async function query(data) {
    const response = await fetch(
        "https://datasets-server.huggingface.co/is-valid?dataset=rotten_tomatoes",
        {
            headers: { Authorization: `Bearer ${API_TOKEN}` },
            method: "GET"
        }
    );
    const result = await response.json();
    return result;
}
query().then((response) => {
    console.log(JSON.stringify(response));
});
```
</js>
<curl>
```curl
curl https://datasets-server.huggingface.co/is-valid?dataset=rotten_tomatoes \
        -X GET \
        -H "Authorization: Bearer ${API_TOKEN}"
```
</curl>
</inferencesnippet>

The response looks like this if a dataset is valid:

```json
{
  "viewer": true,
  "preview": true,
  "search": true,
  "filter": true,
}
```

The response looks like this if a dataset is valid but /search is not available for it:

```json
{
  "viewer": true,
  "preview": true,
  "search": false,
  "filter": true,
}
```

The response looks like this if a dataset is valid but /filter is not available for it:

```json
{
  "viewer": true,
  "preview": true,
  "search": true,
  "filter": false,
}
```

If only the first rows of a dataset are available, then the response looks like:

```json
{
  "viewer": false,
  "preview": true,
  "search": true,
  "filter": true,
}
```

Finally, if the dataset is not valid at all, then the response is:

```json
{
  "viewer": false,
  "preview": false,
  "search": false,
  "filter": false,
}
```

Some cases where a dataset is not valid are:

- the dataset viewer is disabled
- the dataset is gated but the access is not granted: no token is passed or the passed token is not authorized
- the dataset is private but the owner is not a PRO user or an Enterprise Hub org
- the dataset contains no data or the data format is not supported

<Tip>
  Remember if a dataset is <a href="./quick_start#gated-datasets">gated</a>,
  you'll need to provide your user token to submit a successful query!
</Tip>
