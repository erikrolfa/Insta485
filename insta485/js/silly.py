arg_artist = flask.request.args['artist'] 
arg_genre = flask.request.args['genre'] 

connection.execute('''
    SELECT songs.name 
    FROM songs, playlist_contents
    WHERE songs.song_id IN (songs.artist = ? OR songs.genre = ?)
    AND playlist_contents.playlist_name = ?
''',
(arg_artist, arg_genre, playlist ))

song_list = connection.fetchall()

context = {"songlist": songlist, "playlist": playlist, "artist": arg_artist, "genre", arg_genre} 
flask.render_template(playlist.html, **context) 

<body>
    Songs in 485Jam by Hamilton with Genre Hip-Hop:
    {% for songs in songlist %}
        "{{song.name}}"
    Create "Mega-Playlist"
    <form action="/playlist/" method = "POST" enctype="multipart/form-data"/>
    New Playlist Name: <input type="text" name="playlist_name" required/>
    <input type="Sumbit" value="Submit"/>
    </form>

</body>

user = flask.session['logname']
playlist = flask.request.form['playlist_name']


connection.execute('''
    INSERT INTO playlists (name, owner) VALUES (?, ?) 
''',
(user, playlist ))

connection.execute('''
    INSERT INTO playlist_contents (song_id) 
    VALUES (SELECT * FROM songs WHERE )
''',
(user, playlist ))


<div classname="flash-deals">    
    {dealItems.map(item) => (
        <Item

    )}
    <input
            type="Submit"
            value="Add To Cart"
            onClick={(e) => handleAdd(e)}
        </input>
</div>



multiple choice answers:
1 D
2 D
3 C
4 N/A
5 
6
7
8 D
9 A
10 
11
12
13
14
15
16
17
18
19
20

 

 cur = get_db()
 cur.execute('''
    SELECT channels.channel_id
    FROM channels 
    WHERE username = ?
 ''',
 (username, ))
 channel_id = cur.fetchall()

 cur.execute('''
    SELECT youtubers.profile_picture 
    FROM youtubers 
    WHERE username = ?
 ''',
 (username, ))
prof_pic = cur.fetchall()

 channel_id = cur.fetchall()
 cur.execute('''
    SELECT (*) 
    FROM comments 
    WHERE comments.video_id
    IN (SELECT (*) FROM videos 
    WHERE videos.channel_id = ?)
 ''',
 (channel_id['channel_id']))

videos = cur.fetchall()

context = {"username": username, 
            "profile_picture": prof_pic['profile_picture'], 
            "videos": videos}
return flask.render_template(channel.html, **context)


<body>
    <h1> {username} </h1>
    <img src="/uploads/{profile_picture}/" alt="profpic">
    <p>Videos<p>
    {% for video in videos %}
        <img src="/uploads/{video.thumbnail}" alt="thumbnail">
        Comments:
        {%for comment in comments %}


useEffect (() => {
    fetch('/api/v1/tickets',
    .then((response) => {
        if (!response.ok) 
            throw Error.response.statusText);
            return response.json();
    })
    .then((data) => {

    }
    
    )
    )

})