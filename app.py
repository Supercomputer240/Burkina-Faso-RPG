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


# ============================================================
# CUSTOM UI — BURKINA FASO THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(
            135deg,
            #071a12 0%,
            #0b2418 45%,
            #24100f 100%
        );
    color: white;
}


/* ============================================================
   TITLE
   ============================================================ */

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #FCD116;

    text-shadow:
        0px 0px 12px rgba(252, 209, 22, 0.35);

    margin-bottom: 30px;
}


/* ============================================================
   CHARACTER CARDS
   ============================================================ */

.character-card {
    background:
        linear-gradient(
            145deg,
            #10251a,
            #19120f
        );

    border: 2px solid #FCD116;

    border-radius: 18px;

    padding: 20px;

    margin-bottom: 10px;

    box-shadow:
        0px 0px 15px rgba(252, 209, 22, 0.12);
}


.character-name {
    text-align: center;

    font-size: 25px;

    font-weight: 800;

    color: #FCD116;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    width: 100%;

    height: 58px;

    border-radius: 12px;

    font-size: 17px;

    font-weight: 800;

    color: white;

    background-color: #16251c;

    border: 2px solid #009E49;

    transition:
        transform 0.15s,
        background-color 0.15s,
        border-color 0.15s;
}


.stButton > button:hover {

    background-color: #1d3828;

    border-color: #FCD116;

    transform: scale(1.02);

    color: #FCD116;
}


/* ============================================================
   PROGRESS BARS
   ============================================================ */

div[data-testid="stProgress"] > div > div {
    background-color: #009E49;
}


/* ============================================================
   BATTLE LOG
   ============================================================ */

.battle-log {

    background-color:
        rgba(10, 20, 14, 0.9);

    border: 2px solid #EF2B2D;

    border-radius: 15px;

    padding: 18px;

    margin-top: 20px;

    max-height: 300px;

    overflow-y: auto;
}


.log-entry {

    padding: 7px 0;

    border-bottom:
        1px solid rgba(252, 209, 22, 0.12);
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-color:
        rgba(252, 209, 22, 0.35);
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">⚔️ BOSS BATTLE RPG ⚔️</div>',
    unsafe_allow_html=True
)


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


    def crit_check(self, damage):

        if random.random() < 0.20:

            return (
                int(damage * 1.5),
                "🔥 Critical Hit!"
            )

        return damage, ""


    def basic_attack(self, other):

        damage = random.randint(5, 10)

        damage, crit_message = \
            self.crit_check(damage)

        other.health -= damage

        messages = []

        if crit_message:

            messages.append(
                crit_message
            )

        messages.append(
            f"{self.name} punches "
            f"{other.name} for "
            f"{damage} damage!"
        )

        return messages


    def heal(self):

        if self.mana >= 10:

            self.mana -= 10

            heal_amount = random.randint(
                15,
                25
            )

            old_health = self.health

            self.health = min(
                self.health + heal_amount,
                self.max_health
            )

            actual_heal = (
                self.health - old_health
            )

            return True, (
                f"{self.name} heals and restores "
                f"{actual_heal} health."
            )

        return (
            False,
            "Not enough mana to heal."
        )


    def meditate(self):

        regen = random.randint(
            10,
            20
        )

        old_mana = self.mana

        self.mana = min(
            self.mana + regen,
            self.max_mana
        )

        actual_regen = (
            self.mana - old_mana
        )

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

        if random.random() < 0.35:

            return (
                int(damage * 1.5),
                "🔥 Critical Hit!"
            )

        return damage, ""


    def special_attack(self, other):

        if self.mana >= 15:

            damage = random.randint(
                25,
                35
            )

            damage, crit_message = \
                self.crit_check(damage)

            self.mana -= 15

            other.health -= damage

            messages = []

            if crit_message:

                messages.append(
                    crit_message
                )

            messages.append(
                f"{self.name} uses "
                f"⚔️ Warrior Strike "
                f"for {damage} damage!"
            )

            return True, messages

        return False, [
            "Not enough mana for "
            "Warrior Strike."
        ]


# ============================================================
# PALADIN
# ============================================================

class Paladin(Character):

    CLASS_NAME = "Paladin"


    def special_attack(self, other):

        if self.mana >= 15:

            damage = random.randint(
                20,
                35
            )

            damage, crit_message = \
                self.crit_check(damage)

            self.mana -= 15

            other.health -= damage

            messages = []

            if crit_message:

                messages.append(
                    crit_message
                )

            messages.append(
                f"{self.name} unleashes "
                f"✨ Divine Smite "
                f"for {damage} damage!"
            )

            if random.random() < 0.25:

                messages.append(
                    f"⚡ {other.name} is stunned!"
                )

            return True, messages

        return False, [
            "Not enough mana for "
            "Divine Smite."
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
                "💢 The Boss unleashes "
                "Desolation Wave!"
            ]

            damage = random.randint(
                40,
                50
            )

            damage, crit_message = \
                self.crit_check(damage)

            if crit_message:

                messages.append(
                    crit_message
                )

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

        if (
            self.health < 60
            and self.mana >= 10
        ):

            options.append(
                (
                    "heal",
                    40 + (60 - self.health)
                )
            )


        # ----------------------------------------------------
        # MEDITATE
        # ----------------------------------------------------

        if self.mana < 10:

            options.append(
                (
                    "meditate",
                    30 - self.mana
                )
            )


        # ----------------------------------------------------
        # SPECIAL
        # ----------------------------------------------------

        if self.mana >= 20:

            options.append(
                (
                    "special",
                    10 + (100 - target.health)
                )
            )


        # ----------------------------------------------------
        # BASIC ATTACK
        # ----------------------------------------------------

        options.append(
            (
                "basic",
                5 + random.randint(0, 5)
            )
        )


        # ----------------------------------------------------
        # CHOOSE BEST ACTION
        # ----------------------------------------------------

        best = max(
            options,
            key=lambda x: x[1]
        )[0]


        # ----------------------------------------------------
        # PERFORM ACTION
        # ----------------------------------------------------

        if best == "heal":

            success, message = self.heal()

            return [message]


        elif best == "meditate":

            return [
                self.meditate()
            ]


        elif best == "special":

            return self.special_move(
                target
            )


        else:

            return self.basic_attack(
                target
            )


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

    if isinstance(
        messages,
        str
    ):

        st.session_state.battle_log.append(
            messages
        )

    else:

        st.session_state.battle_log.extend(
            messages
        )


def reset_game():

    st.session_state.game_started = False

    st.session_state.player = None

    st.session_state.boss = None

    st.session_state.battle_log = []


def boss_turn():

    player = st.session_state.player

    boss = st.session_state.boss

    if (
        boss.is_alive()
        and player.is_alive()
    ):

        add_messages(
            f"👹 {boss.name}'s turn..."
        )

        boss_messages = \
            boss.choose_ai_action(
                player
            )

        add_messages(
            boss_messages
        )


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.game_started:

    st.subheader(
        "🎮 Start Your Adventure"
    )


    name = st.text_input(
        "Enter your name:"
    )


    class_choice = st.selectbox(
        "Choose your class:",
        [
            "Warrior",
            "Paladin"
        ]
    )


    if st.button(
        "⚔️ Start Battle",
        use_container_width=True
    ):

        if name.strip() == "":

            st.error(
                "Please enter a name."
            )

        else:

            if class_choice == "Warrior":

                player = Warrior(name)

            else:

                player = Paladin(name)


            boss = Boss()


            st.session_state.player = \
                player

            st.session_state.boss = \
                boss


            # ONLY CREATED WHEN GAME STARTS

            st.session_state.battle_log = [

                "⚔️ Battle Start!",

                f"{player.name} enters "
                "the battlefield!",

                "👹 A powerful enemy "
                "stands in your way!"

            ]


            st.session_state.game_started = True

            st.rerun()


# ============================================================
# BATTLE SCREEN
# ============================================================

else:

    player = st.session_state.player

    boss = st.session_state.boss


    # ========================================================
    # PLAYER CARD
    # ========================================================

    st.markdown(
        f"""
        <div class="character-card">
            <div class="character-name">
                🪖 {player.name}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write(
        f"❤️ HP: "
        f"{max(player.health, 0)}"
        f"/{player.max_health}"
    )


    st.progress(
        max(player.health, 0)
        / player.max_health
    )


    st.write(
        f"🔵 Mana: "
        f"{player.mana}"
        f"/{player.max_mana}"
    )


    st.progress(
        player.mana
        / player.max_mana
    )


    st.divider()


    # ========================================================
    # BOSS CARD
    # ========================================================

    st.markdown(
        f"""
        <div class="character-card">
            <div class="character-name">
                👹 {boss.name}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write(
        f"❤️ HP: "
        f"{max(boss.health, 0)}"
        f"/{boss.max_health}"
    )


    st.progress(
        max(boss.health, 0)
        / boss.max_health
    )


    st.write(
        f"🔵 Mana: "
        f"{boss.mana}"
        f"/{boss.max_mana}"
    )


    st.progress(
        boss.mana
        / boss.max_mana
    )


    st.divider()


    # ========================================================
    # GAME OVER
    # ========================================================

    if not player.is_alive():

        st.error(
            f"💀 {player.name} "
            "has been defeated..."
        )


        st.subheader(
            "Game Over"
        )


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
            f"🎉 {boss.name} "
            "has been defeated!"
        )


        st.subheader(
            "🏆 Victory!"
        )


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

                messages = \
                    player.basic_attack(
                        boss
                    )

                add_messages(
                    messages
                )


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

                success, messages = \
                    player.special_attack(
                        boss
                    )

                add_messages(
                    messages
                )


                if (
                    success
                    and boss.is_alive()
                ):

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

                success, message = \
                    player.heal()


                add_messages(
                    message
                )


                # Failed healing does NOT
                # consume a turn

                if (
                    success
                    and boss.is_alive()
                ):

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

                message = \
                    player.meditate()


                add_messages(
                    message
                )


                if boss.is_alive():

                    boss_turn()


                st.rerun()


    # ========================================================
    # BATTLE LOG
    # ========================================================

    st.divider()


    st.subheader(
        "📜 Battle Log"
    )


    log_html = (
        '<div class="battle-log">'
    )


    for message in st.session_state.battle_log:

        log_html += (
            '<div class="log-entry">'
            + str(message)
            + '</div>'
        )


    log_html += (
        '</div>'
    )


    st.markdown(
        log_html,
        unsafe_allow_html=True
    )


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
