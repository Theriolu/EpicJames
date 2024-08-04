<h1 align="center">
  <br>
  <a href="https://github.com/Theriolu/EpicJames"><img src="https://i.imgur.com/CQHRkHE.png" alt="Epic James"></a>
  <br>
  Epic James
  <br>
</h1>

<h4 align="center">Epic giveaway notifications for your discord server!</h4>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.12.4-blue/?logo=python&color=blue&logoColor=FFFFFF">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-yellow.svg" alt="discord.py">
  </a>
  <a href="https://www.postgresql.org/">
     <img src="https://img.shields.io/badge/Postgre-SQL-red/?logo=postgresql&color=red&logoColor=FFFFFF" alt="PostgreSQL">
  </a>
  <a href="https://discord.com/oauth2/authorize?client_id=1268891401836429322&permissions=2147796992&integration_type=0&scope=bot">
     <img src="https://img.shields.io/badge/Add_To_Your_Server_(hosted_by_me)-5865F2/?logo=discord&color=5865F2&logoColor=FFFFFF" alt="Add on discord">
  </a>
</p>
<!-- Content Section -->
<div style="max-width: 800px; margin: 20px auto; padding: 20px; background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
    <p>Epic James is a Discord bot developed in shittiest Python code ever that sends notifications about new free game giveaways in the Epic Games Store directly to your Discord server. Stay updated with the latest free games without any hassle!</p>
    <h2>Features</h2>
    <ul>
        <li>Automatic notifications for new free game giveaways on Epic Games Store.</li>
        <li>Easy to set up and configure in your Discord server.</li>
        <li>Lightweight and unefficient.</li>
        <li>Kinda works.</li>
    </ul>
    <h2>Installation</h2>
    <p>To get Epic James up and running, follow these steps:</p>
    <pre><code>1. Clone the repository:
git clone https://github.com/Theriolu/EpicJames.git

2. Navigate to the project directory:
cd EpicJames

3. Install the required dependencies:
pip install -r requirements.txt

4. Set up your Discord bot token and postgres database in a .env file. Also you can change the flask port in the keep-alive.py

5. Run the bot:
python main.py
</code></pre>
    
    <h2>Configuration</h2>
    <p>Create a <code>.env</code> file in the root directory of the project and add your Discord bot token and other necessary configurations:</p>
    <pre><code>dbname='name of your database'
host='ip/domain of your postgres server (127.0.0.1 if it's running locally)'
password='postgres user password'
port=postgres port
token='your discord bot token'
user='postgres username'
MYGUILD=id of your test server
</code></pre>
    <h2>Usage</h2>
    <p>Once the bot is running, use the /channel command to select a channel for notifications. It will automatically post notifications about new free game giveaways in the specified Discord channel.</p>
    <h2>Contributing</h2>
    <p>We welcome contributions! Feel free to open issues or submit pull requests to improve Epic James.</p>
    <h2>What to improve</h2>
    <ul>
        <li>Make the checkforupdates function more optimized (using timestams from the epic api).</li>
        <li>Add an option to store data in a file instead of a database.</li>
        <li>Remove all of the unnecesaryjunk code (there's a lot of it).</li>
        <li>Implement the future giveaway announcement fuction.</li>
        <li>Use Discord timestamps for the giveaway end date instead of plain text.</li>
        <li>Add some localizations for other languages.</li>
        <li>Fix a bug with adding a new guildvars table entry (it works, but with a weird solution).</li>
    </ul>
    <h2>License</h2>
    <p>This project is licensed under the GPL License. See the <a href="LICENSE">LICENSE</a> file for more details.</p>
    <div style="text-align: center;">
        <p>Made with ❤️ by Theriolu</p>
    </div>
</div>
