package com.bas3d.asrs1

import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.ImageRequest
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_displayr.*
import pl.droidsonroids.gif.GifImageView

class DisplayrActivity : AppCompatActivity(){
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_displayr)
        val gifImageView=findViewById<GifImageView>(R.id.gifImageView)
        gifImageView.visibility= View.GONE

        val idcard1=findViewById<ImageView>(R.id.imageView2)
        val queue1 = Volley.newRequestQueue(this)
        val url1 = "http://$myip/?cmd=FETCHIDCARD1"
        val imageRequest1 = ImageRequest(url1, Response.Listener<Bitmap>
        {response->
            idcard1.setImageBitmap(response)
//
        },187,130, ImageView.ScaleType.CENTER_CROP,null, Response.ErrorListener {
            Toast.makeText(this, "Cannot load image", Toast.LENGTH_LONG).show() })
        imageRequest1.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
        queue1.add(imageRequest1)

        val idcard2=findViewById<ImageView>(R.id.imageView3)
        val queue2 = Volley.newRequestQueue(this)
        val url2="http://$myip/?cmd=FETCHIDCARD2"
        val imageRequest2 = ImageRequest(url2, Response.Listener<Bitmap>
        {response->
            idcard2.setImageBitmap(response)
//
        },187,130, ImageView.ScaleType.CENTER_CROP,null, Response.ErrorListener {
            Toast.makeText(this, "Cannot load image", Toast.LENGTH_LONG).show() })
        imageRequest2.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
        queue2.add(imageRequest2)

        val yes=findViewById<Button>(R.id.button7)
        yes.setOnClickListener {
            gifImageView.visibility= View.VISIBLE
            imageView2.visibility= View.GONE
            imageView3.visibility= View.GONE
            button7.visibility= View.GONE
            button8.visibility= View.GONE
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=SC14CONFIRM"
            val req = JsonObjectRequest(Request.Method.GET, url,null, Response.Listener
            {
                val intent4= Intent(this,RetrieveActivity :: class.java)
                startActivity(intent4)

            }, Response.ErrorListener { Toast.makeText(this, "Error in connection", Toast.LENGTH_LONG).show() })
            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
            queue.add(req)

        }

        val no=findViewById<Button>(R.id.button8)
        no.setOnClickListener {

            val intent8= Intent(this,ScanORuseridActivity::class.java)
            startActivity(intent8)
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