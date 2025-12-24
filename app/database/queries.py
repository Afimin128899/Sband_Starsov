from database.models import User, WithdrawRequest
from sqlalchemy.orm import Session

def get_user(session: Session, user_id: int):
    return session.query(User).filter(User.id == user_id).first()

def create_user(session: Session, user_id: int, full_name: str, username: str = None, invited_by: int = None):
    user = User(id=user_id, full_name=full_name, username=username, invited_by=invited_by)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_balance(session: Session, user_id: int, amount: float):
    user = get_user(session, user_id)
    if user:
        user.balance += amount
        session.commit()
    return user.balance if user else None

def create_withdraw(session: Session, user_id: int, amount: float, target: str):
    wr = WithdrawRequest(user_id=user_id, amount=amount, target=target)
    session.add(wr)
    session.commit()
    session.refresh(wr)
    return wr

def get_withdraws(session: Session, status: str = None):
    query = session.query(WithdrawRequest)
    if status:
        query = query.filter(WithdrawRequest.status == status)
    return query.all()
