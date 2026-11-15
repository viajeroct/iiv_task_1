package app

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.web.bind.annotation.*

@SpringBootApplication
class App

@RestController
class ItemsController(private val jdbc: JdbcTemplate) {
    @GetMapping("/api/items/{id}")
    fun item(@PathVariable id: Long): Map<String, Any?> =
        jdbc.queryForMap("SELECT id, name, payload FROM items WHERE id = ?", id)
}

fun main(args: Array<String>) { runApplication<App>(*args) }
