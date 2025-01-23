import discord
from dotenv import load_dotenv
import os
load_dotenv()

from utils.gen_roll import rng
from utils.bot import bot
from utils.bot import GUILD_ID

from utils.stat_manager import get_character_stats

# Predefined list of characters and their corresponding Discord IDs
character_list = ["Azalea", "Gorwick", "Globius", "Klud", "Mesmir", "Rogath"]
character_ids = [
    os.getenv("AZALEA_ID"), os.getenv("GORWICK_ID"), os.getenv("GLOBIUS_ID"),
    os.getenv("KLUD_ID"), os.getenv("MESMIR_ID"), os.getenv("ROGATH_ID")
]
GM_ID = os.getenv("GM_ID")  # Game Master's Discord ID

class InitiativeMenu(discord.ui.View):
    def __init__(self, character_list, character_ids, gm_id):
        super().__init__()
        self.character_list = character_list
        self.character_ids = character_ids
        self.gm_id = gm_id
        self.initiative_tracker = []
        self.current_turn_index = 0  # Tracks whose turn it is
        self.all_rolled = False
        self.encounter_started = False

        # Add initial buttons
        self.roll_initiative_button = discord.ui.Button(label="Roll Initiative", style=discord.ButtonStyle.blurple, custom_id="roll_initiative")
        self.roll_initiative_button.callback = self.roll_initiative  # Attach callback
        self.add_item(self.roll_initiative_button)

        self.end_turn_button = discord.ui.Button(label="End Turn", style=discord.ButtonStyle.green, custom_id="end_turn", disabled=True)
        self.end_turn_button.callback = self.end_turn
        self.add_item(self.end_turn_button)

        self.end_encounter_button = GMButton(label="End Encounter", custom_id="end_encounter", gm_id=gm_id, style=discord.ButtonStyle.danger, disabled=True)
        self.add_item(self.end_encounter_button)

    async def update_turn_message(self, interaction: discord.Interaction):
        """
        Update the content of the message to notify the next player or show initiative list if not ready.
        """
        if not self.all_rolled:
            # Display initiative list until all rolls are complete
            initiative_list = "\n".join(
                [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in self.initiative_tracker]
            )
            content = f"Waiting for everyone to roll initiative.\n\n**Current Initiative Order:**\n{initiative_list}"
        else:
            # Mention the current player
            current_character = self.initiative_tracker[self.current_turn_index]["character"]
            character_index = self.character_list.index(current_character)
            user_id = self.character_ids[character_index]
            initiative_list = "\n".join(
                [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in self.initiative_tracker]
            )
            content = f"<@{user_id}>, it is your turn now.\n\n**Initiative Order:**\n{initiative_list}"

        await interaction.message.edit(content=content, view=self)

    async def update_buttons(self, interaction: discord.Interaction):
        """
        Update buttons based on the encounter state.
        """
        if self.all_rolled and not self.encounter_started:
            # Update "Roll Initiative" to "Begin Encounter"
            self.roll_initiative_button.label = "Begin Encounter"
            self.roll_initiative_button.style = discord.ButtonStyle.green
            self.roll_initiative_button.disabled = False
        elif self.encounter_started:
            # Remove "Roll Initiative/Begin Encounter" button
            self.remove_item(self.roll_initiative_button)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.custom_id == "end_turn":
                    # Enable for the GM or current player
                    current_character = self.initiative_tracker[self.current_turn_index]["character"]
                    character_index = self.character_list.index(current_character)
                    user_id = self.character_ids[character_index]
                    item.disabled = not self.encounter_started or (str(interaction.user.id) not in [self.gm_id, user_id])
                elif item.custom_id == "end_encounter":
                    item.disabled = not self.encounter_started

        # Update the view
        await self.update_turn_message(interaction)

    async def roll_initiative(self, interaction: discord.Interaction):
        """
        Handle the initiative roll or begin the encounter when everyone has rolled.
        """
        user_id = str(interaction.user.id)

        if self.all_rolled:
            if user_id != self.gm_id:
                await interaction.response.send_message("Only the GM can begin the encounter.", ephemeral=True)
                return

            self.encounter_started = True
            self.end_encounter_button.disabled = False
            self.end_turn_button.disabled = False
            await interaction.response.defer()
            await self.update_buttons(interaction)
            return

        # GM rolls for all characters
        if user_id == self.gm_id:
            rolled_characters = {entry["character"] for entry in self.initiative_tracker}
            remaining_characters = [char for char in self.character_list if char not in rolled_characters]

            for char in remaining_characters:
                stats = get_character_stats(char)
                if stats:
                    modifier = stats.get("initiative modifier", 0)
                else:
                    print(f"Missing stats for {char}")
                    modifier = 0
                roll = rng(20)
                initiative_score = roll + modifier
                self.initiative_tracker.append({"character": char, "initiative": initiative_score})

            self.initiative_tracker = sorted(self.initiative_tracker, key=lambda x: x["initiative"], reverse=True)

            if len(self.initiative_tracker) == len(self.character_list):
                self.all_rolled = True

            tracker_message = "\n".join(
                [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in self.initiative_tracker]
            )

            await interaction.response.edit_message(
                content=f"The GM rolled initiative for the remaining characters.\n\n**Initiative Order:**\n{tracker_message}",
                view=self
            )
            await self.update_buttons(interaction)
            return

        # Player rolls initiative for their character
        if user_id not in self.character_ids:
            await interaction.response.send_message(
                "You are not assigned to any character in this initiative tracker.", ephemeral=True
            )
            return

        character_index = self.character_ids.index(user_id)
        character_name = self.character_list[character_index]

        if any(entry["character"] == character_name for entry in self.initiative_tracker):
            await interaction.response.send_message(
                "You have already rolled initiative.", ephemeral=True
            )
            return

        stats = get_character_stats(character_name)
        if stats:
            modifier = stats.get("initiative modifier", 0)
        else:
            print(f"Missing stats for {character_name}")
            modifier = 0

        roll = rng(20)
        initiative_score = roll + modifier
        self.initiative_tracker.append({"character": character_name, "initiative": initiative_score})

        self.initiative_tracker = sorted(self.initiative_tracker, key=lambda x: x["initiative"], reverse=True)

        if len(self.initiative_tracker) == len(self.character_list):
            self.all_rolled = True

        tracker_message = "\n".join(
            [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in self.initiative_tracker]
        )

        await interaction.response.edit_message(
            content=f"`{character_name}` rolled initiative: 🎲 {roll} + {modifier} = `{initiative_score}`\n\n**Initiative Order:**\n{tracker_message}",
            view=self
        )
        await self.update_buttons(interaction)



    async def end_turn(self, interaction: discord.Interaction):
        """
        Handle ending the current player's turn.
        """
        # Always allow the GM to end the turn
        current_character = self.initiative_tracker[self.current_turn_index]["character"]
        character_index = self.character_list.index(current_character)
        user_id = self.character_ids[character_index]

        if str(interaction.user.id) not in [self.gm_id, user_id]:
            await interaction.response.send_message("You cannot end another player's turn.", ephemeral=True)
            return

        # Cycle to the next turn
        self.current_turn_index = (self.current_turn_index + 1) % len(self.initiative_tracker)

        # Acknowledge the interaction and update the buttons
        await interaction.response.defer()
        await self.update_buttons(interaction)


class GMButton(discord.ui.Button):
    def __init__(self, label, custom_id, gm_id, **kwargs):
        super().__init__(label=label, custom_id=custom_id, **kwargs)
        self.gm_id = gm_id

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.gm_id:
            await interaction.response.send_message("Only the GM can use this button.", ephemeral=True)
            return

        if self.custom_id == "end_encounter":
            await interaction.message.delete()
            await interaction.response.send_message("The encounter has ended. 🎉")


# Slash command to manage initiative
@bot.tree.command(name="initiative", description="Roll initiative and track turn order.", guild=GUILD_ID)
async def initiative(interaction: discord.Interaction, character: str = None):
    """
    Start initiative rolling, or roll for specific/all characters.
    """
    if not hasattr(bot, "initiative_tracker"):
        bot.initiative_tracker = []

    # Default behavior: Start initiative rolling
    if character is None:
        menu = InitiativeMenu(character_list, character_ids, GM_ID)
        await interaction.response.send_message(
            "Click the button below to roll initiative!",
            view=menu
        )
        return

    if character == "All":
        if str(interaction.user.id) == GM_ID:
            bot.initiative_tracker = []
            for char in character_list:
                stats = get_character_stats(char)
                modifier = stats.get("initiative_modifier", 0) if stats else 0
                roll = rng(20)
                initiative_score = roll + modifier
                bot.initiative_tracker.append({"character": char, "initiative": initiative_score})

            bot.initiative_tracker = sorted(bot.initiative_tracker, key=lambda x: x["initiative"], reverse=True)
            tracker_message = "\n".join(
                [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in bot.initiative_tracker]
            )
            await interaction.response.send_message(
                f"Initiative rolled for all characters by the GM.\n\n**Initiative Order:**\n{tracker_message}"
            )
            return
        else:
            await interaction.response.send_message(
                "Only the GM can roll initiative for all characters.", ephemeral=True
            )
            return

    if character not in character_list:
        await interaction.response.send_message("Invalid character name.", ephemeral=True)
        return

    stats = get_character_stats(character)
    modifier = stats.get("initiative_modifier", 0) if stats else 0
    roll = rng(20)
    initiative_score = roll + modifier
    bot.initiative_tracker.append({"character": character, "initiative": initiative_score})
    bot.initiative_tracker = sorted(bot.initiative_tracker, key=lambda x: x["initiative"], reverse=True)
    tracker_message = "\n".join(
        [f"`{entry['character']}`: Initiative `{entry['initiative']}`" for entry in bot.initiative_tracker]
    )
    await interaction.response.send_message(
        f"`{character}` rolled initiative: 🎲 {roll} + {modifier} = `{initiative_score}`\n\n**Initiative Order:**\n{tracker_message}"
    )
