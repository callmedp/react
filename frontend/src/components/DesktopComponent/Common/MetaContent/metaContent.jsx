import React from 'react';
import { Helmet } from 'react-helmet';
import { siteDomain } from 'utils/domains'; 

const MetaContent = props => {
    
    const { meta_tags } = props

    return (
        <Helmet>
            <title>{meta_tags.title}</title>
            <meta name="description" content={meta_tags.description} />
            <meta property="og:title" content={meta_tags.title} />
            <meta property="og:url" content={`${siteDomain}${meta_tags._url}`} />
            <meta property="og:description" content={meta_tags.og_description || meta_tags.description} />
            <meta property="og:type" content={meta_tags.og_type || 'Website'} />
            <meta property="og:site_name" content={meta_tags.site_name || 'ShineLearning'} />
            <meta property="fb:profile_id" content={meta_tags.og_profile_id || ''} />
            {/* <meta property="og:image" content={meta_tags.og_url} /> */}
            <meta itemprop="name" content={meta_tags.title} />
            <meta itemprop="url" content={`${siteDomain}${meta_tags._url}`} />
            <meta itemprop="description" content={meta_tags.og_description || meta_tags.description} />
            <link rel="canonical" href={`${siteDomain}${meta_tags._url}`} />
            <meta name="twitter:card" content="summary" />
            <meta name="twitter:domain" content={siteDomain} />
            <meta name="twitter:site" content="@shinelearning" />
            <meta name="twitter:title" content={meta_tags.title} />
            <meta name="twitter:url" content={`${siteDomain}${meta_tags._url}`} />
            <meta name="twitter:description" content={meta_tags.description} />
        </Helmet>
        
    )
}

export default MetaContent;