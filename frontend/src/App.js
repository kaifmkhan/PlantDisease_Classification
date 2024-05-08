import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";

// import Home from "./home";
import { ImageUpload } from "./diseaseClass";

function App() {
    return (
        <Router>
            <Routes>
                {/* <Route exact path="/" element={<Home />} /> */}
                <Route path="/" element={<ImageUpload />} />

            </Routes>
        </Router>
    );
}

export default App;