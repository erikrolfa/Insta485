import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

export default function Feed({ url }) {
  const [postMap, setPostMap] = useState([]);
  const [nextUrl, setNextUrl] = useState("");
  const [hasNext, setHasNext] = useState(false);

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
          setPostMap(data.results);
          setNextUrl(data.next);
          if (data.next !== "") {
            setHasNext(true);
          }
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

  function fetchData() {
    console.log("NEXT URL ", nextUrl);
    // Call REST API to get the post's information
    if (hasNext === true) {
      fetch(nextUrl, {
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setNextUrl(data.next);
          setPostMap([...posts, ...data.results]);
          console.log(data.url);
          if (data.next === "") {
            setHasNext(false);
          }
        })
        .catch((error) => console.log(error));
    }
  }

  const posts = postMap.map((post) => (
    <Post key={post.postid} url={post.url} />
  ));

  return (
    <div>
      <InfiniteScroll
        dataLength={posts.length}
        next={() => fetchData()}
        hasMore={hasNext}
        loader={<h4>Loading...</h4>}
      >
        {posts}
      </InfiniteScroll>
    </div>
  );
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};
