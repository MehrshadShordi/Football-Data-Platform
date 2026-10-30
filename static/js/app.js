async function LoadMatches() {
    const response = await fetch("/api/matches");
    const leagues = await response.json();

    const container = document.getElementById("leagues");
    container.innerHTML = "";

    for (const league of leagues) {
        const leagueCardElement = document.createElement("div");
        leagueCardElement.className = "league_card";
        const LeagueElement = document.createElement("div");
        LeagueElement.id = "league";
        const LeagueNameElement = document.createElement("h5");
        const LeagueIconElement = document.createElement("img");
        LeagueIconElement.src = `https://images.fotmob.com/image_resources/logo/leaguelogo/${league.league_id}_small.png`;
        LeagueIconElement.className = "team_logo"
        LeagueNameElement.textContent = `${league.league}`;

        LeagueElement.appendChild(LeagueIconElement);
        LeagueElement.appendChild(LeagueNameElement);
        leagueCardElement.appendChild(LeagueElement);

        for (const match of league.matches) {
            const MatchCardElement = document.createElement("div");
            MatchCardElement.className = "match_card";
            const HomeNameDiv = document.createElement("div");
            const HomeImgDiv = document.createElement("div");
            const HomeTeamImg = document.createElement("img");
            HomeTeamImg.className = "team_logo";
            HomeTeamImg.src = `https://images.fotmob.com/image_resources/logo/teamlogo/${match.home_id}_small.png`;
            HomeTeamImg.onerror = function () {
                this.onerror = null;
                this.src = '/static/default_team.png';

            };
            const HomeTeamName = document.createElement("h6");
            HomeTeamName.textContent = `${match.home}`;
            HomeImgDiv.appendChild(HomeTeamImg);
            HomeNameDiv.appendChild(HomeTeamName);



            const ResultDiv = document.createElement("div");
            if (match.finished == "true") {
                const HomeTeamScore = document.createElement("h6");
                HomeTeamScore.textContent = `${match.home_score}`;
                const AwayTeamScore = document.createElement("h6");
                AwayTeamScore.textContent = `${match.away_score}`;
                ResultDiv.appendChild(HomeTeamScore);
                ResultDiv.appendChild(AwayTeamScore);
            } else if (match.started == true) {
                const HomeTeamScore = document.createElement("h6");
                HomeTeamScore.textContent = `${match.home_score}`;
                const GameTime = document.createElement("h6");
                GameTime.textContent = `${match.reason}`;
                const AwayTeamScore = document.createElement("h6");
                AwayTeamScore.textContent = `${match.away_score}`;
                ResultDiv.appendChild(HomeTeamScore);
                ResultDiv.appendChild(GameTime);
                ResultDiv.appendChild(AwayTeamScore);
            } else if (match.cancelled == true) {
                const GameReason = document.createElement("h6");
                GameReason.textContent = `${match.reason}`;
                ResultDiv.appendChild(GameReason);
            } else {
                const GameTime = document.createElement("h6");
                GameTime.textContent = `${match.time}`;
                ResultDiv.appendChild(GameTime);
            }

            const AwayNameDiv = document.createElement("div");
            const AwayImgDiv = document.createElement("div");
            const AwayTeamImg = document.createElement("img");
            AwayTeamImg.className = "team_logo";
            AwayTeamImg.src = `https://images.fotmob.com/image_resources/logo/teamlogo/${match.away_id}_small.png`;
            AwayTeamImg.onerror = function () {
                this.onerror = null;
                this.src = '/static/default_team.png';

            };
            const AwayTeamName = document.createElement("h6");
            AwayTeamName.textContent = `${match.away}`;
            AwayNameDiv.appendChild(AwayTeamName);
            AwayImgDiv.appendChild(AwayTeamImg);

            MatchCardElement.appendChild(HomeImgDiv);
            MatchCardElement.appendChild(HomeNameDiv);
            MatchCardElement.appendChild(ResultDiv);
            MatchCardElement.appendChild(AwayNameDiv);
            MatchCardElement.appendChild(AwayImgDiv);
            leagueCardElement.appendChild(MatchCardElement);
        }
        container.appendChild(leagueCardElement);
    }

}

LoadMatches();
setInterval(LoadMatches, 60000);