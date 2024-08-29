from django.utils import timezone

# FInance App common context
def common(request):
    now = timezone.now()

    return {"now_year": now.year,
            "now_month": now.month}