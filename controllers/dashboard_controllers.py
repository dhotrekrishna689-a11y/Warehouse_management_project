from services import dashboard_services


def get_dashboard_data():
    dashboard_data = dashboard_services.get_dashboard_data()

    return {
        "data": dashboard_data,
        "message": "Dashboard data fetched successfully"
    }, 200