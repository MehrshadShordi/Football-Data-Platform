async function LoadMatches() {
    const response = await fetch("/api/matches");
    const leagues = await response.json();

    const container = document.getElementById("matches_container");
    container.innerHTML = "";

    for (const league of leagues){
        const leagueElement = document.createElement("section");

        const leagueTitle = document.createElement("h2");
        leagueTitle.textContent = league.league;

        leagueElement.appendChild(leagueTitle);

        for (const match of league.matches){
            const matchElement = document.createElement("p");

            matchElement.textContent = `${match.home} ${match.home_score} - ${match.away_score} ${match.away}`;

            leagueElement.appendChild(matchElement);

        }
        container.appendChild(leagueElement);
    }

}

LoadMatches();
setInterval(LoadMatches,60000);