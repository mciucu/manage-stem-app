import {UI, Route} from "UI";
import {IndexPage} from "./IndexPage";
import {BlogRoute} from "BlogPanel";
import {ForumRoute} from "ForumPanel";

export const MAIN_ROUTE = new Route(null, IndexPage, [
    new BlogRoute(),
    new ForumRoute(),
]);
