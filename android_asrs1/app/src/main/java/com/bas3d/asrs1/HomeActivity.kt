package com.bas3d.asrs1

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_sandr.*
import org.json.JSONObject

class HomeActivity : AppCompatActivity() {
    val myip=Global().ip
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
        val start = findViewById<Button>(R.id.button)
        start.setOnClickListener {
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=GETCOUNT"
            val req = JsonObjectRequest(Request.Method.GET, url,null,Response.Listener<JSONObject>
            {
                val intent = Intent(this, SandRActivity()::class.java)
                startActivity(intent)

            }, Response.ErrorListener {
                Intent(this, SandRActivity()::class.java).also {
                    startActivity(it)
                    Toast.makeText(this,"Cannot Initiate Storage-Slots are full", Toast.LENGTH_SHORT).show()  }

            })

            queue.add(req)

        }
    }

    override fun onBackPressed() {

        val a = Intent(Intent.ACTION_MAIN)
        a.addCategory(Intent.CATEGORY_HOME)
        a.flags = Intent.FLAG_ACTIVITY_NEW_TASK
        startActivity(a)
    }


}