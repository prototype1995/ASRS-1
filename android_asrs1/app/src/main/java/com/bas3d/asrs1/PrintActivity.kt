package com.bas3d.asrs1

import android.content.Intent
import android.graphics.Bitmap
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
import com.android.volley.toolbox.ImageRequest
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

class PrintActivity : AppCompatActivity() {
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_print)
        val progressBar=findViewById<ProgressBar>(R.id.progressBar)
        progressBar.visibility= GONE
        val qrcode=findViewById<ImageView>(R.id.imageView4)
        val queue1 = Volley.newRequestQueue(this)
        val url1 = "http://$myip/?cmd=FETCHQRCODE"
        val imageRequest1 = ImageRequest(url1, Response.Listener<Bitmap>
        {response->
            qrcode.setImageBitmap(response)
        },187,130, ImageView.ScaleType.CENTER_CROP,null,
            Response.ErrorListener {
                Toast.makeText(this, "Cannot load image", Toast.LENGTH_LONG).show() })
        queue1.add(imageRequest1)

        val yesprint=findViewById<Button>(R.id.button11)
        val noprint=findViewById<Button>(R.id.button12)
        yesprint.setOnClickListener {
            progressBar.visibility= VISIBLE
            yesprint.isEnabled=false
            noprint.isEnabled=false
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=PRINT"
            val stringRequest = StringRequest(Request.Method.GET, url, Response.Listener<String>
            {
                val i= Intent(this,SmsActivity::class.java)
                startActivity(i)

            }, Response.ErrorListener {

                Toast.makeText(this,"Can't print", Toast.LENGTH_SHORT).show()  })

            stringRequest.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)

            queue.add(stringRequest)
        }

        noprint.setOnClickListener {
            yesprint.isEnabled=false
            noprint.isEnabled=false
            val queue2 = Volley.newRequestQueue(this)
            val url2 = "http://$myip/?cmd=SC7CONFIRM"
            val req = JsonObjectRequest(Request.Method.GET, url2,null, Response.Listener {
                val intent8= Intent(this,SmsActivity::class.java)
                startActivity(intent8)
            }, Response.ErrorListener { error ->
                Toast.makeText(applicationContext, error.message, Toast.LENGTH_SHORT).show()  })
            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)

            queue2.add(req)
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