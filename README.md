```grocery_tracker/
├── alembic/                      # Alembic migration files
│   ├── versions/                 # Versioned migration scripts
│   └── env.py                    # Alembic environment configuration
├── app/
│   ├── api/                      # API endpoints
│   │   ├── v1/                   # Versioning for APIs
│   │   │   ├── endpoints/        # API route files
│   │   │   │   ├── users.py      # User-related routes
│   │   │   │   ├── orders.py     # Order-related routes
│   │   │   │   └── analytics.py  # Analytics-related routes
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/                     # Core application functionality
│   │   ├── config.py             # App configuration
│   │   ├── security.py           # Authentication/authorization logic
│   │   └── __init__.py
│   ├── db/                       # Database-related files
│   │   ├── base.py               # Base models for ORM
│   │   ├── session.py            # DB session and engine creation
│   │   ├── models/               # ORM models
│   │   │   ├── user.py           # User model
│   │   │   ├── order.py          # Order model
│   │   │   ├── item.py           # Item model
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── services/                 # Business logic
│   │   ├── order_service.py      # Order processing logic
│   │   ├── analytics_service.py  # Analytics and insights logic
│   │   └── __init__.py
│   ├── schemas/                  # Pydantic models for validation
│   │   ├── user.py               # User-related schemas
│   │   ├── order.py              # Order-related schemas
│   │   └── __init__.py
│   ├── utils/                    # Utility functions
│   │   ├── ocr.py                # OCR-related functions
│   │   ├── notifications.py      # Notification-related functions
│   │   └── __init__.py
│   ├── main.py                   # Entry point for FastAPI
│   └── __init__.py
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── __init__.py
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation
```


```
Field Name	Description
Order ID	A unique identifier for each order.
User ID	The identifier of the user who placed the order.
Order Date	The date when the order was placed.
Platform	The service or platform through which the order was made (e.g., Zepto, Blinkit, Amazon).
Item Name	The name of the product purchased in the order.
Category	The category under which the item falls (e.g., Dairy, Staples, Fruits).
Quantity	The number of units of the item purchased.
Unit Price	The price of a single unit of the item.
Total Price	The total price for the quantity purchased (Quantity * Unit Price).
Payment Method	The method used to pay for the order (e.g., Credit Card, UPI, Cash).
Discount	Any discount applied to the order (in monetary value).
Final Price	The final amount to be paid after applying discounts.
Order Source	The origin of the order, such as online, app-based, or in-store purchase.

```