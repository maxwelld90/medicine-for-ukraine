import React, { useState, useEffect } from "react";
import './progressBar.css';

export default function ProgressBar({ currentStep = 0 }) {
    console.log(currentStep);
    return ( <
        div className = { "progress " + ("step" + currentStep) } > < /div>
    );
}