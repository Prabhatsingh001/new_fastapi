

auth_prefix = "/api/v1/auth"

def test_user_creation(fake_session, fake_user_service, test_client):
    response = test_client.post(
        url = f"{auth_prefix}/signup",
        json={

        },
    )