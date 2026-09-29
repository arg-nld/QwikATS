from app.database.session import SessionLocal
from app.models.tenant import Tenant


def test_database():
    db = SessionLocal()

    try:
        tenant = Tenant(
            name="QwikATS Demo Company",
            slug="qwikats-demo",
        )

        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        print("Tenant created successfully!")
        print(f"ID: {tenant.id}")
        print(f"Name: {tenant.name}")
        print(f"Slug: {tenant.slug}")

    finally:
        db.close()


if __name__ == "__main__":
    test_database()