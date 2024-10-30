import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */
  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  const [created, setCreated] = useState("");
  const [postShowUrl, setPostShowUrl] = useState("");
  const [comments, setComments] = useState([]);
  const [lognameLikesThis, setLognameLikesThis] = useState(false);
  const [numLikes, setNumLikes] = useState(0);
  const [urll, setUrll] = useState("");
  const [postId, setPostId] = useState(98);
  const [dataFilled, setDataFilled] = useState(false);

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    // Call REST API to get the post's information
    fetch(url, { method: "GET", credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          setOwnerImgUrl(data.ownerImgUrl);
          setCreated(data.created);
          setOwnerShowUrl(data.ownerShowUrl);
          setPostShowUrl(data.postShowUrl);
          setComments(data.comments);
          setLognameLikesThis(data.likes.lognameLikesThis);
          setNumLikes(data.likes.numLikes);
          setUrll(data.likes.url);
          setPostId(data.postid);
          setDataFilled(true);
        }
      })
      .catch((error) => console.log(error));

    
    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  function dblLike() {
    if (lognameLikesThis === false) {
      // Call REST API to get the post's information
      const text = `/api/v1/likes/?postid=${postId.toString()}`;
      fetch(text, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setNumLikes(numLikes + 1);
          setLognameLikesThis(true);
          setUrll(data.url);
        })
        .catch((error) => console.log(error));
    }
  }

  function buttLike() {
    if (lognameLikesThis === true) {
      // Call REST API to get the post's information
      fetch(urll, { credentials: "same-origin", method: "DELETE" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          setNumLikes(numLikes - 1);
          setLognameLikesThis(!lognameLikesThis);
        })
        .catch((error) => console.log(error));
    } else {
      // Call REST API to get the post's information
      console.log("JIM", postId);
      const text = `/api/v1/likes/?postid=${postId.toString()}`;
      fetch(text, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setNumLikes(numLikes + 1);
          setLognameLikesThis(!lognameLikesThis);
          setUrll(data.url);
        })
        .catch((error) => console.log(error));
    }
  }

  function deleteComment(com, e) {
    e.preventDefault();
    console.log("deletecommentid", com.commentid);
    // Call REST API to get the post's information
    fetch(com.url, {
      method: "DELETE",
      credentials: "same-origin",
    })
      .then((response) => {
        console.log("hello world", response);
        if (!response.ok) throw Error(response.statusText);
        setComments(
          comments.filter((comment) => comment.commentid !== com.commentid),
        );
      })
      .catch((error) => console.log(error));
  }

  // Render post image and post owner
  return (
      <div>
      {dataFilled ? (
        <div className="post">
        <a href={ownerShowUrl}>
          <img src={ownerImgUrl} width={100} height={100} alt="Profile Pic" />
        </a>
        <a href={ownerShowUrl}>
          <p>{owner}</p>
        </a>
        <img src={imgUrl} alt="post_image" onDoubleClick={dblLike} />
        <p>{numLikes}</p>
        <p>{numLikes !== 1 ? " likes" : " like"}</p>
        <button type="button" data-testid="like-unlike-button" onClick={buttLike}>
          {lognameLikesThis ? "unlike" : "like"}
        </button>
        <a href={postShowUrl}>
          <p>{dayjs(created).utc(true).local().fromNow()}</p>
        </a>
        <div className="comTot">
          {comments.map((comment) => (
            <div key={comment.commentid}>
              <a href={comment.ownerShowUrl}>
                <p>{comment.owner}</p>
              </a>
              <span data-testid="comment-text">{comment.text}</span>
              <p>
                {comment.lognameOwnsThis && (
                  <button
                    type="button"
                    data-testid="delete-comment-button"
                    onClick={(e) => deleteComment(comment, e)}
                  >
                    <p>delete comment</p>
                  </button>
                )}
              </p>
            </div>
          ))}
        </div>
        <div>
          <PostComment
            comPostId={postId}
            setComments={setComments}
            comments={comments}
          />
        </div>
        <br />
      </div>
        ) : (
        <p> Loading... </p>
      )}
    </div>
  );
}

function PostComment({ comPostId, setComments, comments }) {
  const [text, setText] = useState("");

  useEffect(() => () => {}, [comPostId, text]);

  const onFormSubmit = (e) => {
    e.preventDefault();
    const tex = `/api/v1/comments/?postid=${comPostId.toString()}`;
    fetch(tex, {
      method: "POST",
      body: JSON.stringify({ text }),
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log("commentid", data.commentid);
        setText("");
        setComments(
          comments.concat({
            commentid: data.commentid,
            lognameOwnsThis: data.lognameOwnsThis,
            owner: data.owner,
            ownerShowUrl: data.ownerShowUrl,
            text: data.text,
            url: data.url,
          }),
        );
      })
      .catch((error) => console.log(error));
  };

  return (
    <div>
      <form data-testid="comment-form" onSubmit={onFormSubmit}>
        <input
          data-testid="comment-form"
          type="text"
          onChange={(e) => setText(e.target.value)}
        />
      </form>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

PostComment.propTypes = {
  comPostId: PropTypes.number.isRequired,
  setComments: PropTypes.func.isRequired,
  comments: PropTypes.array.isRequired,
};
