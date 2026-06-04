# Database Design

## Users

| Field | Type |
|---------|---------|
| id | INT |
| name | VARCHAR(100) |
| email | VARCHAR(100) |
| password | VARCHAR(255) |
| role | VARCHAR(50) |

---

## Categories

| Field | Type |
|---------|---------|
| id | INT |
| name | VARCHAR(100) |
| description | TEXT |

---

## Assets

| Field | Type |
|---------|---------|
| id | INT |
| asset_tag | VARCHAR(50) |
| name | VARCHAR(100) |
| brand | VARCHAR(100) |
| model | VARCHAR(100) |
| serial_number | VARCHAR(100) |
| category_id | INT |
| status | VARCHAR(50) |
| location | VARCHAR(100) |
| purchase_date | DATE |
| warranty_expiration | DATE |
| notes | TEXT |

---

## Interventions

| Field | Type |
|---------|---------|
| id | INT |
| asset_id | INT |
| description | TEXT |
| intervention_date | DATE |
| technician | VARCHAR(100) |
