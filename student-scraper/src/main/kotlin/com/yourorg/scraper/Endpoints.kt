package com.yourorg.scraper

data class Endpoints(
    val baseUrl: String,
    val login: String,
    val attendance: String,
    val marks: String,
    val timetable: String,
    val captchaSolverUrl: String
) {
    companion object {
        fun default() = Endpoints(
            baseUrl = "https://vtop.vitap.ac.in",
            login = "/vtop/login",
            attendance = "/vtop/attendance",
            marks = "/vtop/marks",
            timetable = "/vtop/timetable",
            captchaSolverUrl = "https://api.example.com/solve"
        )
    }
}
