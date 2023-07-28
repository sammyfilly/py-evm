import pytest

from eth.vm.forks.frontier.computation import (
    FrontierComputation,
)
from eth.vm.message import (
    Message,
)


@pytest.fixture
def state(chain_without_block_validation, canonical_address_a):
    state = chain_without_block_validation.get_vm().state
    state.set_balance(canonical_address_a, 1000)
    return state


@pytest.fixture
def message(canonical_address_a, canonical_address_b):
    return Message(
        to=canonical_address_a,
        sender=canonical_address_b,
        value=100,
        data=b"",
        code=b"",
        gas=100,
    )


@pytest.fixture
def computation(message, transaction_context, state):
    return FrontierComputation(
        state=state,
        message=message,
        transaction_context=transaction_context,
    )


@pytest.fixture
def child_message(computation, canonical_address_b):
    return computation.prepare_child_message(
        gas=100, to=canonical_address_b, value=200, data=b"", code=b""
    )


@pytest.fixture
def child_computation(computation, child_message):
    return computation.generate_child_computation(child_message)


def test_generate_child_computation(computation, child_computation):
    assert (
        computation.transaction_context.gas_price
        == child_computation.transaction_context.gas_price
    )
    assert (
        computation.transaction_context.origin
        == child_computation.transaction_context.origin
    )
