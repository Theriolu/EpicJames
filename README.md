<!-- Banner Section -->
<div style="width: 100%; height: 200px; background-color: #4caf50; display: flex; justify-content: center; align-items: center; color: white; font-size: 2.5em; text-transform: uppercase; font-weight: bold;">
</div>

<!-- Content Section -->
<div style="max-width: 800px; margin: 20px auto; padding: 20px; background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
    <h1 style="text-align: center;">Epic James</h1>
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
    <h2>License</h2>
    <p>This project is licensed under the GPL License. See the <a href="LICENSE">LICENSE</a> file for more details.</p>
    <div style="text-align: center;">
        <p>Made with ❤️ by Theriolu</p>
    </div>
</div>
