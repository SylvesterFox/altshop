from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from remnawave.enums.users import TrafficLimitStrategy

from src.api.presenters.user_account import build_subscription_response
from src.core.enums import PlanType, SubscriptionStatus
from src.core.utils.time import datetime_now
from src.infrastructure.database.models.dto import PlanSnapshotDto, SubscriptionDto


def test_build_subscription_response_uses_effective_expired_status() -> None:
    plan = PlanSnapshotDto(
        id=1,
        name="Starter",
        tag="starter",
        type=PlanType.BOTH,
        traffic_limit=100,
        device_limit=1,
        duration=30,
        traffic_limit_strategy=TrafficLimitStrategy.NO_RESET,
        internal_squads=[],
        external_squad=None,
    )
    subscription = SubscriptionDto(
        id=10,
        user_remna_id=UUID("00000000-0000-0000-0000-000000000010"),
        user_telegram_id=7766264322,
        status=SubscriptionStatus.ACTIVE,
        traffic_limit=100,
        device_limit=1,
        internal_squads=[],
        external_squad=None,
        expire_at=datetime_now() - timedelta(minutes=1),
        url="https://example.test/sub",
        plan=plan,
    )

    response = build_subscription_response(subscription)

    assert response.status == "EXPIRED"
