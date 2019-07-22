package com.bas3d.asrs1

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.text.TextUtils
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley

class ThankuActivity : AppCompatActivity() {
    val myip=Global().ip
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_thanku)
        val textView=findViewById<TextView>(R.id.textView11)
        textView.ellipsize = TextUtils.TruncateAt.MARQUEE
        Toast.makeText(this,"Your card stored successfully", Toast.LENGTH_SHORT).show()
        val mhandler= Handler()
        mhandler.postDelayed({run{
            doStuff() }
        },8000)

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

    private fun doStuff()
    {
        val intent4= Intent(this,HomeActivity :: class.java)
        startActivity(intent4)
    }

    override fun onBackPressed() {

    }
}