document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("fetchButton").addEventListener("click", async (event) => {
        event.preventDefault();  // Prevents unexpected form submission
        const username = document.getElementById("githubUsername").value.trim();
        if (!username) {
            alert("Please enter a GitHub username!");
            return;
        }

        try {
            const response = await fetch(`https://api.github.com/users/${username}/events`);
            if (!response.ok) throw new Error("GitHub API Error");

            const events = await response.json();
            const commitEvents = events.filter(e => e.type === "PushEvent");

            if (commitEvents.length === 0) {
                document.getElementById("output").textContent = "No commits found!";
                return;
            }

            // Reverse commit order
            const reversedCommits = commitEvents.map(event => {
                return event.payload.commits.map(commit => commit.message).reverse();
            }).flat();

            document.getElementById("output").textContent = reversedCommits.join("\n");
        } catch (error) {
            document.getElementById("output").textContent = "Error fetching commits!";
            console.error(error);
        }
    });
});
