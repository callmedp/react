import React, { useState } from 'react';
import './features.scss'

export default function Features(){
    return (

<section class="howItWork">
<div class="container h-100">
    <div class="row h-100 howItWork__wrap">
        <div class="col-md-3 h-100">
            <div class="d-flex flex-column align-items-center">
                <i class="sprite layout-resume"></i>
                <p class="mb-0 mt-3 font-weight-bold text-center">Better formatting <br/>&amp; layout of Resume</p>
            </div>
        </div>
        <div class="col-md-3 h-100">
            <div class="d-flex flex-column align-items-center">
                <i class="sprite tips"></i>
                <p class="mb-0 mt-3 font-weight-bold text-center">Tips to improve the <br/>resume to stand you out</p>
            </div>
        </div>
        <div class="col-md-3 h-100">
            <div class="d-flex flex-column align-items-center">
                <i class="sprite review-score"></i>
                <p class="mb-0 mt-3 font-weight-bold text-center">Detailed review of <br/>each section with score</p>
            </div>
        </div>
        <div class="col-md-3 h-100">
            <div class="d-flex flex-column align-items-center">
                <i class="sprite expert-guidance"></i>
                <p class="mb-0 mt-3 font-weight-bold text-center">Expert Guidance to <br/>increase resume views</p>
            </div>
        </div>
    </div>
</div>
</section>
    );
}