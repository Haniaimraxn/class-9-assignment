

import streamlit as st
from abc import ABC, abstractmethod
import hashlib

# ---------------------------
# Simulated Database
# ---------------------------
class Database:
    def __init__(self):
        self.users = {}  # {username: User}
        self.plans = {}  # {user_id: List[Plan]}

    def add_user(self, user):
        self.users[user.username] = user

    def get_user(self, username: str):
        return self.users.get(username)

    def save_plan(self, user_id: str, plan):
        if user_id not in self.plans:
            self.plans[user_id] = []
        self.plans[user_id].append(plan)

# ---------------------------
# Auth System
# ---------------------------
class Auth:
    def __init__(self, db: Database):
        self.db = db

    def register(self, username: str, password: str) -> bool:
        if username in self.db.users:
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User(username, hashed_password)
        self.db.add_user(user)
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.db.get_user(username)
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return user.password == hashed_password
        return False

# ---------------------------
# Payment
# ---------------------------
class PaymentProcessor:
    def process_payment(self, user_id: str, amount: float, plan_type: str) -> bool:
        st.success(f"Processed payment of ${amount} for {plan_type} for user {user_id}")
        return True

# ---------------------------
# User Class
# ---------------------------
class User:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._goals = {}

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    def set_goals(self, weight: float, goal_type: str):
        self._goals = {"weight": weight, "type": goal_type}

    def get_goals(self):
        return self._goals

# ---------------------------
# Abstract Plan
# ---------------------------
class Plan(ABC):
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

    @abstractmethod
    def generate_plan(self) -> str:
        pass

class StrengthPlan(Plan):
    def generate_plan(self) -> str:
        return f"Strength Plan: {self.name} - Squats, Deadlifts, Bench Press for {self.duration} weeks"

class VeganMealPlan(Plan):
    def generate_plan(self) -> str:
        return f"Vegan Meal Plan: {self.name} - Tofu Stir-fry, Lentil Soup for {self.duration} days"

# ---------------------------
# App Class
# ---------------------------
class FitTrackr:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if "db" not in st.session_state:
            st.session_state.db = Database()
            st.session_state.auth = Auth(st.session_state.db)
            st.session_state.payment = PaymentProcessor()
        if "current_user" not in st.session_state:
            st.session_state.current_user = None

    def run(self):
        st.title("FitTrackr - Your Fitness Journey")

        # Login/Register
        if not st.session_state.current_user:
            st.subheader("Login or Register")
            action = st.radio("Choose action", ["Login", "Register"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if action == "Register" and st.button("Register"):
                if st.session_state.auth.register(username, password):
                    st.success("Registered successfully! Please log in.")
                else:
                    st.error("Username already exists.")

            if action == "Login" and st.button("Login"):
                if st.session_state.auth.login(username, password):
                    st.session_state.current_user = st.session_state.db.get_user(username)
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        # Main App
        if st.session_state.current_user:
            user = st.session_state.current_user
            st.subheader(f"Welcome, {user.username}")

            goal_type = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain"])
            weight = st.number_input("Target Weight (kg)", min_value=40.0, max_value=200.0)

            if st.button("Set Goals"):
                user.set_goals(weight, goal_type)
                st.success("Goals updated!")

            if st.button("Subscribe to Premium ($9.99/month)"):
                if st.session_state.payment.process_payment(user.username, 9.99, "Premium"):
                    st.success("Subscribed to Premium!")

            plan_type = st.selectbox("Choose Plan", ["Strength Workout", "Vegan Meal"])
            duration = st.slider("Plan Duration (weeks)", 1, 12, 4)

            if st.button("Generate Plan"):
                if plan_type == "Strength Workout":
                    plan = StrengthPlan("Strength Training", duration)
                else:
                    plan = VeganMealPlan("Vegan Nutrition", duration)
                st.session_state.db.save_plan(user.username, plan)
                st.write(plan.generate_plan())

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app = FitTrackr()
    app.run()



