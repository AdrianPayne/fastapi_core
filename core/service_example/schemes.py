from .models import HeroBase, Team


class TeamRead(Team):
    pass


class HeroCreate(HeroBase):
    password: str


class HeroUpdate(HeroBase):
    name: str | None
    team_id: str | None


class HeroRead(HeroBase):
    id: int
    team: TeamRead | None = None
