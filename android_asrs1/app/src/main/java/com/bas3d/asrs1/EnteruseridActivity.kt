package com.bas3d.asrs1

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

class EnteruseridActivity : AppCompatActivity() {
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_userid)

        val edittext=findViewById<EditText>(R.id.editText)
        val uid=edittext.text
        val submit=findViewById<Button>(R.id.button9)
        submit.setOnClickListener {
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=VALIDATEUID&uid=$uid"
            val stringRequest = StringRequest(Request.Method.GET, url, Response.Listener<String>
            {
                val i = Intent(this, DisplayrActivity::class.java)
                startActivity(i)

            }, Response.ErrorListener {

                Toast.makeText(applicationContext, "Invalid Visitor's Receipt ID", Toast.LENGTH_SHORT).show()  })

            queue.add(stringRequest)
        }
        val exit=findViewById<ImageView>(R.id.imageView15)
        exit.setOnClickListener {
            exit.alpha=0.5f
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=AUTOHOME"
            val req = JsonObjectRequest(Request.Method.GET, url,null, Response.Listener
            {

                val intent= Intent(this,HomeActivity::class.java)
                startActivity(intent)

            }, Response.ErrorListener { error ->
                Toast.makeText(applicationContext, error.message, Toast.LENGTH_SHORT).show()  })
            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)

            queue.add(req)
        }

    }

    override fun onBackPressed() {

    }
}