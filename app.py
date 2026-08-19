import streamlit as st
import random


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Boss Battle RPG",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔️ Boss Battle RPG")

# ============================================================
# CUSTOM UI
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #0e1117;
    }

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 30px;
    }

    .character-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .character-name {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }

    .battle-log {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 15px;
        height: 250px;
        overflow-y: auto;
    }

    .stButton > button {
        width: 100%;
        height: 55px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: bold;
        border: 1px solid #444;
        background-color: #21262d;
        color: white;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #30363d;
        border-color: #888;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# BASE CHARACTER CLASS
# ============================================================

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50

    def is_alive(self):
        return self.health > 0

    def status(self):
        return (
            f"{self.name} ➤ "
            f"HP: {self.health}/{self.max_health} | "
            f"Mana: {self.mana}/{self.max_mana}"
        )

    def crit_check(self, damage):
        """20% chance to deal 1.5x damage."""
        if random.random() < 0.20:
            return int(damage * 1.5), "🔥 Critical Hit!"
        return damage, ""

    def basic_attack(self, other):
        damage = random.randint(5, 10)

        damage, crit_message = self.crit_check(damage)

        other.health -= damage

        messages = []

        if crit_message:
            messages.append(crit_message)

        messages.append(
            f"{self.name} punches {other.name} for {damage} damage!"
        )

        return messages

    def heal(self):
        if self.mana >= 10:
            self.mana -= 10

            heal_amount = random.randint(15, 25)
            old_health = self.health

            self.health = min(
                self.health + heal_amount,
                self.max_health
            )

            actual_heal = self.health - old_health

            return True, (
                f"{self.name} heals and restores "
                f"{actual_heal} health."
            )

        return False, "Not enough mana to heal."

    def meditate(self):
        regen = random.randint(10, 20)

        old_mana = self.mana

        self.mana = min(
            self.mana + regen,
            self.max_mana
        )

        actual_regen = self.mana - old_mana

        return (
            f"{self.name} meditates and restores "
            f"{actual_regen} mana."
        )


# ============================================================
# WARRIOR
# ============================================================

class Warrior(Character):

    CLASS_NAME = "Warrior"

    def crit_check(self, damage):
        """35% chance to deal 1.5x damage."""
        if random.random() < 0.35:
            return int(damage * 1.5), "🔥 Critical Hit!"

        return damage, ""

    def special_attack(self, other):

        if self.mana >= 15:

            damage = random.randint(25, 35)

            damage, crit_message = self.crit_check(damage)

            self.mana -= 15
            other.health -= damage

            messages = []

            if crit_message:
                messages.append(crit_message)

            messages.append(
                f"{self.name} uses ⚔️ Warrior Strike "
                f"for {damage} damage!"
            )

            return True, messages

        return False, [
            "Not enough mana for Warrior Strike."
        ]


# ============================================================
# PALADIN
# ============================================================

class Paladin(Character):

    CLASS_NAME = "Paladin"

    def special_attack(self, other):

        if self.mana >= 15:

            damage = random.randint(20, 35)

            damage, crit_message = self.crit_check(damage)

            self.mana -= 15
            other.health -= damage

            messages = []

            if crit_message:
                messages.append(crit_message)

            messages.append(
                f"{self.name} unleashes ✨ Divine Smite "
                f"for {damage} damage!"
            )

            if random.random() < 0.25:
                messages.append(
                    f"⚡ {other.name} is stunned!"
                )

            return True, messages

        return False, [
            "Not enough mana for Divine Smite."
        ]


# ============================================================
# BOSS
# ============================================================

class Boss(Character):

    def __init__(self):

        super().__init__("The Boss")

        self.health = 150
        self.max_health = 150

        self.mana = 40
        self.max_mana = 40

    def special_move(self, target):

        if self.mana >= 20:

            messages = [
                "💢 The Boss unleashes Desolation Wave!"
            ]

            damage = random.randint(40, 50)

            damage, crit_message = self.crit_check(damage)

            if crit_message:
                messages.append(crit_message)

            self.mana -= 20
            target.health -= damage

            messages.append(
                f"💀 {target.name} is hit for "
                f"{damage} massive damage!"
            )

            return messages

        return self.basic_attack(target)

    def choose_ai_action(self, target):

        options = []

        # ----------------------------------------------------
        # HEAL
        # ----------------------------------------------------

        if self.health < 60 and self.mana >= 10:
            options.append(
                ("heal", 40 + (60 - self.health))
            )

        # ----------------------------------------------------
        # MEDITATE
        # ----------------------------------------------------

        if self.mana < 10:
            options.append(
                ("meditate", 30 - self.mana)
            )

        # ----------------------------------------------------
        # SPECIAL
        # ----------------------------------------------------

        if self.mana >= 20:
            options.append(
                ("special", 10 + (100 - target.health))
            )

        # ----------------------------------------------------
        # BASIC ATTACK
        # ----------------------------------------------------

        options.append(
            ("basic", 5 + random.randint(0, 5))
        )

        # Choose highest score
        best = max(
            options,
            key=lambda x: x[1]
        )[0]

        # Perform action
        if best == "heal":

            success, message = self.heal()

            return [message]

        elif best == "meditate":

            return [self.meditate()]

        elif best == "special":

            return self.special_move(target)

        else:

            return self.basic_attack(target)


# ============================================================
# SESSION STATE
# ============================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "player" not in st.session_state:
    st.session_state.player = None

if "boss" not in st.session_state:
    st.session_state.boss = None

if "battle_log" not in st.session_state:
    st.session_state.battle_log = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_messages(messages):

    if isinstance(messages, str):
        st.session_state.battle_log.append(messages)

    else:
        st.session_state.battle_log.extend(messages)


def reset_game():

    st.session_state.game_started = False
    st.session_state.player = None
    st.session_state.boss = None
    st.session_state.battle_log = []


def boss_turn():

    player = st.session_state.player
    boss = st.session_state.boss

    if boss.is_alive() and player.is_alive():

        add_messages(f"👹 {boss.name}'s turn...")

        boss_messages = boss.choose_ai_action(player)

        add_messages(boss_messages)


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.game_started:

    st.subheader("🎮 Start Your Adventure")

    name = st.text_input(
        "Enter your name:"
    )

    class_choice = st.selectbox(
        "Choose your class:",
        ["Warrior", "Paladin"]
    )

    if st.button(
        "⚔️ Start Battle",
        use_container_width=True
    ):

        if name.strip() == "":
            st.error("Please enter a name.")

        else:

            # Create player
            if class_choice == "Warrior":
                player = Warrior(name)
            else:
                player = Paladin(name)

            # Create boss
            boss = Boss()

            # Save the game
            st.session_state.player = player
            st.session_state.boss = boss

            # IMPORTANT:
            # These messages are created ONLY ONCE,
            # when the battle begins.
            st.session_state.battle_log = [
                "⚔️ Battle Start!",
                f"{player.name} enters the battlefield!",
                "👹 A powerful enemy stands in your way!"
            ]

            st.session_state.game_started = True

            st.rerun()


# ============================================================
# BATTLE SCREEN
# ============================================================

else:

    player = st.session_state.player
    boss = st.session_state.boss

    # --------------------------------------------------------
    # PLAYER STATUS
    # --------------------------------------------------------

    st.subheader(f"🪖 {player.name}")

    st.progress(
        max(player.health, 0) / player.max_health
    )

    st.write(
        f"❤️ HP: {max(player.health, 0)}/{player.max_health}"
    )

    st.progress(
        player.mana / player.max_mana
    )

    st.write(
        f"🔵 Mana: {player.mana}/{player.max_mana}"
    )

    st.divider()

    # --------------------------------------------------------
    # BOSS STATUS
    # --------------------------------------------------------

    st.subheader(f"👹 {boss.name}")

    st.progress(
        max(boss.health, 0) / boss.max_health
    )

    st.write(
        f"❤️ HP: {max(boss.health, 0)}/{boss.max_health}"
    )

    st.progress(
        boss.mana / boss.max_mana
    )

    st.write(
        f"🔵 Mana: {boss.mana}/{boss.max_mana}"
    )

    st.divider()


    # ========================================================
    # GAME OVER
    # ========================================================

    if not player.is_alive():

        st.error(
            f"💀 {player.name} has been defeated..."
        )

        st.subheader("Game Over")

        if st.button(
            "🔄 Restart",
            use_container_width=True
        ):

            reset_game()

            st.rerun()


    # ========================================================
    # VICTORY
    # ========================================================

    elif not boss.is_alive():

        st.success(
            f"🎉 {boss.name} has been defeated!"
        )

        st.subheader("🏆 Victory!")

        if st.button(
            "🔄 Play Again",
            use_container_width=True
        ):

            reset_game()

            st.rerun()


    # ========================================================
    # PLAYER TURN
    # ========================================================

    else:

        st.subheader(
            f"🎯 {player.name}'s Turn"
        )

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # BASIC ATTACK
        # ----------------------------------------------------

        with col1:

            if st.button(
                "👊 Basic Attack",
                use_container_width=True
            ):

                messages = player.basic_attack(boss)

                add_messages(messages)

                if boss.is_alive():

                    boss_turn()

                st.rerun()


        # ----------------------------------------------------
        # SPECIAL ATTACK
        # ----------------------------------------------------

        with col2:

            if st.button(
                "⚡ Special Attack",
                use_container_width=True
            ):

                success, messages = player.special_attack(boss)

                add_messages(messages)

                # Only successful attacks use a turn
                if success and boss.is_alive():

                    boss_turn()

                st.rerun()


        # ----------------------------------------------------
        # HEAL
        # ----------------------------------------------------

        with col1:

            if st.button(
                "❤️ Heal (10 Mana)",
                use_container_width=True
            ):

                success, message = player.heal()

                add_messages(message)

                # Failed healing DOES NOT use a turn
                if success and boss.is_alive():

                    boss_turn()

                st.rerun()


        # ----------------------------------------------------
        # MEDITATE
        # ----------------------------------------------------

        with col2:

            if st.button(
                "🔵 Meditate",
                use_container_width=True
            ):

                message = player.meditate()

                add_messages(message)

                if boss.is_alive():

                    boss_turn()

                st.rerun()


    # ========================================================
    # BATTLE LOG
    # ========================================================

    st.divider()

    st.subheader("📜 Battle Log")

    for message in st.session_state.battle_log:

        st.write(message)


    # ========================================================
    # RESTART GAME
    # ========================================================

    st.divider()

    if st.button(
        "🔄 Restart Game",
        use_container_width=True
    ):

        reset_game()

        st.rerun()
