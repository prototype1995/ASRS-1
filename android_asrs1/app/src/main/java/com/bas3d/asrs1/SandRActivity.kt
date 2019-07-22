package com.bas3d.asrs1

import android.content.Intent
import android.os.Bundle
import android.view.View.GONE
import android.view.View.VISIBLE
import android.widget.Button
import android.widget.ImageView
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley

class SandRActivity : AppCompatActivity() {
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sandr)
        val store=findViewById<Button>(R.id.button2)
        val retrieve=findViewById<Button>(R.id.button3)
        val exit=findViewById<ImageView>(R.id.imageView15)
        val progressBar=findViewById<ProgressBar>(R.id.progressBar2)
        progressBar.visibility=GONE
        store.setOnClickListener {
            progressBar.visibility=VISIBLE
            store.isEnabled=false
            retrieve.isEnabled=false
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=SC2STORE"
            val req = JsonObjectRequest(Request.Method.GET, url, null, Response.Listener
            {

                val intent2 = Intent(this, InsertActivity::class.java)
                startActivity(intent2)


            }, Response.ErrorListener {

                Toast.makeText(applicationContext,"Error in connection", Toast.LENGTH_LONG).show()  })


            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
            queue.add(req)
        }
        retrieve.setOnClickListener {
            store.isEnabled=false
            retrieve.isEnabled=false
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=AUTOHOME"
            val req = JsonObjectRequest(Request.Method.GET, url, null, Response.Listener
            {

                val intent3= Intent(this,ScanORuseridActivity::class.java)
                startActivity(intent3)

            }, Response.ErrorListener {

                Toast.makeText(applicationContext, "Error in connection", Toast.LENGTH_SHORT).show()  })


            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
            queue.add(req)
        }

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