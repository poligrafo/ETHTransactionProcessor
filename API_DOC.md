## 1. List Transactions

**Endpoint**: GET /

**Description**: Retrieve a list of transactions, with optional filtering by `from_address`, `to_address`, and `block_number`.

**Query Parameters**:
- `skip` (int): Number of records to skip (default: 0).
- `limit` (int): Maximum number of records to return (default: 50).
- `from_address` (str, optional): Filter by sender address.
- `to_address` (str, optional): Filter by recipient address.
- `block_number` (int, optional): Filter by block number.

**Response**:
- `200 OK`: A list of transactions.

**Example Response**:
```json
[
    {
        "hash": "0x1234abcd...",
        "from_address": "0xabc123...",
        "to_address": "0xdef456...",
        "value": 1000000000000000000,
        "gas": 21000,
        "gas_price": 50000000000,
        "block_number": 12345678,
        "transaction_type": "transfer"
    },
    ...
]
```
**Curl Command**:
```bash
curl -X GET "http://localhost:8000/?skip=0&limit=10&from_address=0xabc123..." -H "accept: application/json"
```

This complete document now includes all three endpoints and can be used as your `.md` file content for the API documentation.


## 2. Get Transaction Stats

**Endpoint**: GET /stats

**Description**: Retrieve statistics for the transactions.

**Response**:
- `200 OK`: Statistics including the total count of transactions and average gas price.

**Example Response**:
```json
{
    "total_count": 1000,
    "avg_gas_price": 25000000000.0
}
```
**Curl Command**:
```bash
curl -X GET "http://localhost:8000/stats" -H "accept: application/json"
```

This snippet provides the documentation for the "Get Transaction Stats" endpoint in the desired format.


## 3. Get Transaction by Hash

**Endpoint**: GET /{tx_hash}

**Description**: Retrieve a specific transaction by its hash.

**Path Parameter**:
- `tx_hash` (str): The hash of the transaction to retrieve.

**Response**:
- `200 OK`: The transaction details.
- `404 Not Found`: If the transaction with the given hash does not exist.

**Example Response**:
```json
{
    "hash": "0x1234abcd...",
    "from_address": "0xabc123...",
    "to_address": "0xdef456...",
    "value": 1000000000000000000,
    "gas": 21000,
    "gas_price": 50000000000,
    "block_number": 12345678,
    "transaction_type": "transfer"
}
```
**Curl Command**:
```bash
curl -X GET "http://localhost:8000/0x1234abcd..." -H "accept: application/json"
```
This completes the documentation for the "Get Transaction by Hash" endpoint in the requested format.

## Notes:
### 1. Caching: The responses from these endpoints may be cached for up to 24 hours to improve performance.
### 2. Error Handling: Ensure you handle potential 404 errors when querying a specific transaction by hash.