package com.yourorg.scraper

data class StudentData(
    val attendance: List<Attendance>,
    val marks: List<Mark>,
    val timetable: List<TimetableEntry>
)

data class Attendance(
    val courseCode: String,
    val courseName: String,
    val attended: Int,
    val total: Int,
    val percentage: Int
)

data class Mark(
    val courseCode: String,
    val score: String
)

data class TimetableEntry(
    val day: String,
    val slot: String,
    val courseCode: String
)
