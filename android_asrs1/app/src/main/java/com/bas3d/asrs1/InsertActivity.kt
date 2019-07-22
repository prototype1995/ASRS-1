package com.bas3d.asrs1

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_insert.*
import pl.droidsonroids.gif.GifImageView

class InsertActivity : AppCompatActivity() {
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_insert)
        val cont=findViewById<Button>(R.id.button4)
        val textview=findViewById<TextView>(R.id.textView7)
        val gifImageView=findViewById<GifImageView>(R.id.gifImageView)
        gifImageView.visibility= View.GONE
        cont.setOnClickListener {
            val queue = Volley.newRequestQueue(this)
            val url = "http://$myip/?cmd=DETECTCARD"
            val req = StringRequest(Request.Method.GET, url, Response.Listener<String>
            {response->
                if(response=="True")
                {
                    gifImageView.visibility= View.VISIBLE
                    textView.visibility= View.GONE
                    button4.visibility= View.GONE
                    textview.visibility = View.GONE
                    val queue1 = Volley.newRequestQueue(this)
                    val url1 = "http://$myip/?cmd=SC3CONTINUE"
                    val req = JsonObjectRequest(Request.Method.GET, url1,null, Response.Listener
                    {
                        val intent1 = Intent(this,DisplayActivity::class.java)
                        startActivity(intent1)

                    }, Response.ErrorListener {

                        Toast.makeText(this,"Please wait", Toast.LENGTH_SHORT).show()  })
                    req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)


                    queue1.add(req)
                }

            }, Response.ErrorListener {

                textview.visibility = View.VISIBLE


            })
            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)

            queue.add(req)
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