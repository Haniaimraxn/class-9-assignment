
import streamlit as st
from abc import ABC, abstractmethod
import hashlib

# Simulated Database (Dictionary-based)
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

# Authentication System
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

# Payment System (Simulated)
class PaymentProcessor:
    def process_payment(self, user_id: str, amount: float, plan_type: str) -> bool:
        # Simulate payment processing
        st.success(f"Processed payment of ${amount} for {plan_type} for user {user_id}")
        return True

# User Class
class User:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._goals = {}  # e.g., {"weight": 70, "type": "loss"}

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

# Abstract Plan Class
class Plan(ABC):
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

    @abstractmethod
    def generate_plan(self) -> str:
        pass

# Concrete Plan Classes
class StrengthPlan(Plan):
    def generate_plan(self) -> str:
        return f"Strength Plan: {self.name} - Squats, Deadlifts, Bench Press for {self.duration} weeks"

class VeganMealPlan(Plan):
    def generate_plan(self) -> str:
        return f"Vegan Meal Plan: {self.name} - Tofu Stir-fry, Lentil Soup for {self.duration} days"

# Main Application
class FitTrackr:
    def __init__(self):
        self.db = Database()
        self.auth = Auth(self.db)
        self.payment_processor = PaymentProcessor()
        self.current_user = None

    def run(self):
        st.title("FitTrackr - Your Fitness Journey")
        
        # Authentication UI
        if not self.current_user:                   
            st.subheader("Login or Register")
            action = st.radio("Choose action", ["Login", "Register"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if action == "Register" and st.button("Register"):
                if self.auth.register(username, password):
                    st.success("Registered successfully! Please log in.")
                else:
                    st.error("Username already exists.")
            
            if action == "Login" and st.button("Login"):
                if self.auth.login(username, password):
                    self.current_user = self.db.get_user(username)
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Invalid credentials.")
        
        # Main App Features
        if self.current_user:
            st.subheader(f"Welcome, {self.current_user.username}")
            goal_type = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain"])
            weight = st.number_input("Target Weight (kg)", min_value=40.0, max_value=200.0)
            
            if st.button("Set Goals"):
                self.current_user.set_goals(weight, goal_type)
                st.success("Goals updated!")
            
            # Simulate Subscription
            if st.button("Subscribe to Premium ($9.99/month)"):
                if self.payment_processor.process_payment(self.current_user.username, 9.99, "Premium"):
                    st.success("Subscribed to Premium!")
            
            # Generate Plans
            plan_type = st.selectbox("Choose Plan", ["Strength Workout", "Vegan Meal"])
            duration = st.slider("Plan Duration (weeks)", 1, 12, 4)
            
            if st.button("Generate Plan"):
                if plan_type == "Strength Workout":
                    plan = StrengthPlan("Strength Training", duration)
                else:
                    plan = VeganMealPlan("Vegan Nutrition", duration)
                self.db.save_plan(self.current_user.username, plan)
                st.write(plan.generate_plan())

if __name__ == "__main__":
    app = FitTrackr()
    app.run()

