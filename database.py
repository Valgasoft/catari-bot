# Cat Bot - A Discord bot about catching cats.
# Copyright (C) 2025 Lia Milenakos & Cat Bot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import config
import peewee
import playhouse.sqlite_ext
import playhouse.postgres_ext

if config.DB_TYPE == "SQLITE":
    db = playhouse.sqlite_ext.SqliteExtDatabase("catbot.db", pragmas=(("cache_size", -1024 * 64), ("journal_mode", "wal")))
elif config.DB_TYPE == "POSTGRES":
    db = playhouse.postgres_ext.PostgresqlExtDatabase("cat_bot", user="cat_bot", password=config.DB_PASS, host="localhost", port=5432)

cattypes = [
    "Regular": 1500,
    "Fine": 1000,
    "Nice": 750,
    "Good": 500,
    "Rare": 350,
    "Wild": 275,
    "Baby": 230,
    "Epic": 200,
    "Sus": 175,
    "Brave": 150,
    "Rickroll": 125,
    "Reverse": 100,
    "Superior": 80,
    "Coward": 70,
    "Katari": 60 # KAT ari
    "Trash": 50,
    "Legendary": 35,
    "Mythic": 25,
    "8bit": 20,
    "Corrupt": 15,
    "Professor": 10,
    "Divine": 8,
    "Total": 7,
    "Sandpile": 6
    "Real": 5,
    "Best": 4,
    "Ultimate": 3,
    "eGirl": 2,
    "Unreal": 1,
    "Glitched": 0.5,
    "Impossible": 0.01,
    "Amazing": 0.005,
    "Fantastic": 0.001,
]


class CappedIntegerField(peewee.IntegerField):
    MAX_VALUE = 2147483647
    MIN_VALUE = -2147483648

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_value(self, value):
        if value is not None:
            return max(self.MIN_VALUE, min(self.MAX_VALUE, value))
        return value


class Profile(peewee.Model):
    user_id = peewee.BigIntegerField()
    guild_id = peewee.BigIntegerField(index=True)

    time = peewee.FloatField(default=99999999999999)  # fastest catch time
    timeslow = peewee.FloatField(default=0)  # slowest catch time

    timeout = peewee.BigIntegerField(default=0)  # /preventcatch timestamp
    cataine_active = peewee.BigIntegerField(default=0)  # cataine timestamp

    dark_market_level = peewee.SmallIntegerField(default=0)  # dark market level
    dark_market_active = peewee.BooleanField(default=False)  # dark market unlocked bool
    story_complete = peewee.BooleanField(default=False)  # whether story is complete

    finale_seen = peewee.BooleanField(default=False)  # whether the finale cutscene was seen
    debt_seen = peewee.BooleanField(default=False)  # whether the debt cutscene was seen

    cataine_week = peewee.SmallIntegerField(default=0)  # light market purcashes this week
    recent_week = peewee.SmallIntegerField(default=0)  # the week

    funny = peewee.SmallIntegerField(default=0)  # private embed click amount
    facts = peewee.SmallIntegerField(default=0)  # /fact amount
    gambles = peewee.SmallIntegerField(default=0)  # casino spins amount

    cookies = peewee.BigIntegerField(default=0)  # cookies clicked

    rain_minutes = peewee.SmallIntegerField(default=0)  # server-locked rains amount

    slot_spins = peewee.IntegerField(default=0)
    slot_wins = peewee.IntegerField(default=0)
    slot_big_wins = peewee.SmallIntegerField(default=0)

    battlepass = peewee.SmallIntegerField(default=0)  # battlepass level
    progress = peewee.SmallIntegerField(default=0)  # battlepass progress (in xp)
    season = peewee.SmallIntegerField(default=0)  # if this doesnt match current season it will reset everything

    # battelpass quests fields
    vote_reward = peewee.SmallIntegerField(default=0)
    vote_cooldown = peewee.BigIntegerField(default=1)

    catch_quest = peewee.CharField(default="", max_length=30)
    catch_progress = peewee.SmallIntegerField(default=0)
    catch_cooldown = peewee.BigIntegerField(default=1)
    catch_reward = peewee.SmallIntegerField(default=0)

    misc_quest = peewee.CharField(default="", max_length=30)
    misc_progress = peewee.SmallIntegerField(default=0)
    misc_cooldown = peewee.BigIntegerField(default=1)
    misc_reward = peewee.SmallIntegerField(default=0)

    bp_history = peewee.CharField(default="")

    reminder_catch = peewee.BigIntegerField(default=0)  # timestamp of last catch reminder
    reminder_misc = peewee.BigIntegerField(default=0)  # timestamp of last misc reminder
    # vote timestamp is in the User model

    reminders_enabled = peewee.BooleanField(default=False)

    highlighted_stat = peewee.CharField(default="time_records", max_length=30)

    # advanced stats
    boosted_catches = peewee.IntegerField(default=0)  # amount of catches boosted by prism
    cataine_activations = peewee.IntegerField(default=0)  # amount of cataine activations
    cataine_bought = peewee.IntegerField(default=0)  # amount of cataine bought
    quests_completed = peewee.IntegerField(default=0)  # amount of quests completed
    total_catches = peewee.IntegerField(default=0)  # total amount of catches
    total_catch_time = peewee.BigIntegerField(default=0)  # total amount of time spent catching
    perfection_count = peewee.IntegerField(default=0)  # amount of perfection achievements
    rain_participations = peewee.IntegerField(default=0)  # amount of catches during rains
    rain_minutes_started = peewee.IntegerField(default=0)  # amount of rain minutes started
    reminders_set = peewee.IntegerField(default=0)  # amount of reminders set
    cats_gifted = CappedIntegerField(default=0)  # amount of cats gifted
    cat_gifts_recieved = CappedIntegerField(default=0)  # amount of cat gifts recieved
    trades_completed = peewee.IntegerField(default=0)  # amount of trades completed
    cats_traded = CappedIntegerField(default=0)  # amount of cats traded
    ttt_played = peewee.IntegerField(default=0)  # amount of times played the TTT
    ttt_won = peewee.IntegerField(default=0)  # amount of TTT wins
    ttt_draws = peewee.IntegerField(default=0)  # amount of TTT draws
    packs_opened = peewee.IntegerField(default=0)  # amount of packs opened
    pack_upgrades = peewee.IntegerField(default=0)  # amount of pack upgrades
    new_user = peewee.BooleanField(default=True)  # whether the user is new

    puzzle_pieces = peewee.IntegerField(default=0)  # amount of puzzle pieces collected for birthday 2025 event

    # thanks chatgpt
    # cat types
    for cattype in cattypes:
        locals()[f"cat_{cattype}"] = CappedIntegerField(default=0)

    # aches
    with open("config/aches.json", "r") as f:
        ach_list = json.load(f)
    for ach in ach_list.keys():
        locals()[ach] = peewee.BooleanField(default=False)

    # packs
    for pack in ["Wooden", "Stone", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Celestial"]:
        locals()[f"pack_{pack.lower()}"] = peewee.IntegerField(default=0)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

    class Meta:
        # haha facebook meta reference
        database = db
        only_save_dirty = True
        indexes = ((("user_id", "guild_id"), True),)


class User(peewee.Model):
    user_id = peewee.BigIntegerField(unique=True, index=True, primary_key=True)

    vote_time_topgg = peewee.BigIntegerField(default=0)  # timestamp of last vote
    reminder_vote = peewee.BigIntegerField(default=0)  # timestamp of last vote reminder

    custom = peewee.CharField(default="")  # custom cat name
    custom_num = peewee.IntegerField(default=1)  # custom cat amount
    emoji = peewee.CharField(default="")  # /editprofile emoji
    color = peewee.CharField(default="")  # /editprofile color
    image = peewee.CharField(default="")  # /editprofile image

    rain_minutes = peewee.SmallIntegerField(default=0)  # rain minute balance
    premium = peewee.BooleanField(default=False)  # whether the user has supporter
    claimed_free_rain = peewee.BooleanField(default=False)  # whether the user has claimed their free rain

    news_state = peewee.CharField(default="", max_length=2000)

    # advanced stats
    total_votes = peewee.IntegerField(default=0)  # total amount of votes
    max_vote_streak = peewee.IntegerField(default=0)  # max vote streak
    vote_streak = peewee.IntegerField(default=0)  # current vote streak

    class Meta:
        database = db
        only_save_dirty = True


class Channel(peewee.Model):
    channel_id = peewee.BigIntegerField(unique=True, index=True, primary_key=True)

    cat = peewee.BigIntegerField(default=0)  # cat message id
    cattype = peewee.CharField(default="", max_length=20)  # curently spawned cat type (parsed from msg if none)
    forcespawned = peewee.BooleanField(default=False)  # whether the current cat is forcespawned

    thread_mappings = peewee.BooleanField(default=False)  # whether the channel is a thread

    spawn_times_min = peewee.BigIntegerField(default=120)  # spawn times minimum
    spawn_times_max = peewee.BigIntegerField(default=1200)  # spawn times maximum

    lastcatches = peewee.BigIntegerField(default=0)  # timestamp of last catch
    yet_to_spawn = peewee.BigIntegerField(default=0)  # timestamp of the next catch, if any
    cat_rains = peewee.BigIntegerField(default=0)  # timestamp of rain end, if any

    appear = peewee.CharField(default="", max_length=4000)
    cought = peewee.CharField(default="", max_length=4000)

    webhook = peewee.CharField(default="")  # webhook url

    class Meta:
        database = db
        only_save_dirty = True


class Prism(peewee.Model):
    user_id = peewee.BigIntegerField()
    guild_id = peewee.BigIntegerField(index=True)

    time = peewee.BigIntegerField()  # creation time
    creator = peewee.BigIntegerField()  # original crafter
    name = peewee.CharField(max_length=20)  # name (duh)

    catches_boosted = peewee.IntegerField(default=0)  # amount of boosts from catches

    for cattype in cattypes:  # enabled boosts
        locals()[f"enabled_{cattype.lower()}"] = peewee.BooleanField(default=True)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

    class Meta:
        database = db
        only_save_dirty = True
        indexes = ((("user_id", "guild_id"), False),)


class Reminder(peewee.Model):
    user_id = peewee.BigIntegerField()
    time = peewee.BigIntegerField(index=True)
    text = peewee.CharField(max_length=2000)

    class Meta:
        database = db
        only_save_dirty = True
