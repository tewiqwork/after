import aiosqlite

class DB:
    def __init__(self, path):
        self.path = path

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.executescript("""
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
            CREATE TABLE IF NOT EXISTS warnings(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild INTEGER NOT NULL,
                user INTEGER NOT NULL,
                mod INTEGER NOT NULL,
                reason TEXT NOT NULL,
                created INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_warn ON warnings(guild,user);
            CREATE TABLE IF NOT EXISTS clans(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild INTEGER NOT NULL,
                name TEXT NOT NULL,
                tag TEXT NOT NULL,
                owner INTEGER NOT NULL,
                role INTEGER
            );
            CREATE TABLE IF NOT EXISTS clan_members(
                clan INTEGER NOT NULL,
                user INTEGER NOT NULL,
                PRIMARY KEY(clan,user)
            );
            CREATE TABLE IF NOT EXISTS config(
                guild INTEGER PRIMARY KEY,
                create_voice INTEGER
            );
            """)

    async def add_warn(self,g,u,m,r,t):
        async with aiosqlite.connect(self.path) as db:
            cur=await db.execute(
                "INSERT INTO warnings(guild,user,mod,reason,created) VALUES(?,?,?,?,?)",
                (g,u,m,r,t)
            )
            await db.commit()
            return cur.lastrowid

    async def warn_count(self,g,u):
        async with aiosqlite.connect(self.path) as db:
            cur=await db.execute("SELECT COUNT(*) FROM warnings WHERE guild=? AND user=?",(g,u))
            return (await cur.fetchone())[0]

    async def warns(self,g,u,limit=10):
        async with aiosqlite.connect(self.path) as db:
            cur=await db.execute(
                "SELECT id,mod,reason,created FROM warnings WHERE guild=? AND user=? ORDER BY id DESC LIMIT ?",
                (g,u,limit)
            )
            return await cur.fetchall()

    async def clan(self,g,u):
        async with aiosqlite.connect(self.path) as db:
            cur=await db.execute(
                """SELECT c.id,c.name,c.tag,c.owner,c.role
                   FROM clans c JOIN clan_members m ON c.id=m.clan
                   WHERE c.guild=? AND m.user=?""",(g,u))
            return await cur.fetchone()

    async def create_clan(self,g,name,tag,owner,role):
        async with aiosqlite.connect(self.path) as db:
            cur=await db.execute(
                "INSERT INTO clans(guild,name,tag,owner,role) VALUES(?,?,?,?,?)",
                (g,name,tag,owner,role)
            )
            cid=cur.lastrowid
            await db.execute("INSERT INTO clan_members VALUES(?,?)",(cid,owner))
            await db.commit()
            return cid

    async def add_member(self,cid,uid):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT OR IGNORE INTO clan_members VALUES(?,?)",(cid,uid))
            await db.commit()

    async def remove_member(self,cid,uid):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("DELETE FROM clan_members WHERE clan=? AND user=?",(cid,uid))
            await db.commit()

    async def delete_clan(self,cid):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("DELETE FROM clan_members WHERE clan=?",(cid,))
            await db.execute("DELETE FROM clans WHERE id=?",(cid,))
            await db.commit()

    async def set_voice(self,g,cid):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO config(guild,create_voice) VALUES(?,?) "
                "ON CONFLICT(guild) DO UPDATE SET create_voice=excluded.create_voice",
                (g,cid)
            )
            await db.commit()

    async def voice(self,g):
        async with aiosqlite.connect(self.path) as db:
            cur=await db.execute("SELECT create_voice FROM config WHERE guild=?",(g,))
            row=await cur.fetchone()
            return row[0] if row else None
