from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Session

sqlite_database = 'sqlite:///tgbot.db'

engine = create_engine(sqlite_database, echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer)
    requests = Column(Integer, default=999)
    
    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    request_text = Column(String)
    answer_text = Column(String)
    user = relationship('User', back_populates='messages')


with Session(autoflush=False, bind=engine) as db:
    async def add_user(tg_id): # Добавляем нового пользователя в бд, если не существует
        user = db.query(User).filter(User.tg_id==tg_id).first()
        if not user:
            user = User(tg_id=tg_id)
            db.add(user)
            db.commit()
            db.close()
    
    async def made_request(tg_id, request_text, answer_text):
        user = db.query(User).filter(User.tg_id==tg_id).first()
        if user:
            user.requests -= 1
            new_message = Message(request_text=request_text, answer_text=answer_text, user=user)
            db.add(new_message)
            db.commit()
            db.close()
    
    async def get_users():
        users = []
        all_users = db.query(User).all()
        for user in all_users:
            users.append(user.tg_id)
        return users
    
    async def get_requests(tg_id):
        user = db.query(User).filter(User.tg_id==tg_id).first()
        if user:
            return user.requests
    
    
    async def user_history(tg_id):
        user = db.query(User).filter(User.tg_id == tg_id).first()
        if user:
            messages = (db.query(Message).filter(Message.user_id == user.id).order_by(Message.id.desc()).limit(5).all())
            context = ""
            for message in reversed(messages):  # Переворачиваем список для хронологии
                context += f"\n\nЗапрос: {message.request_text}\nОтвет: {message.answer_text}"
            return context

