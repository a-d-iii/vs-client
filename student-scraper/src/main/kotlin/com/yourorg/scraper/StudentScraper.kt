package com.yourorg.scraper

interface StudentScraper {
    suspend fun fetchAll(
        credentials: Credentials,
        captchaSolver: CaptchaSolver,
        endpoints: Endpoints = Endpoints.default()
    ): ScrapeResult
}
