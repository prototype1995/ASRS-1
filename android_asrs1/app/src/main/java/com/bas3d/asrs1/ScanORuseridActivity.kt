package com.bas3d.asrs1

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.google.zxing.integration.android.IntentIntegrator

class ScanORuseridActivity : AppCompatActivity(){
    val myip=Global().ip
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_scanoruserid)
        val scan=findViewById<Button>(R.id.button5)
        scan.setOnClickListener{
            val scanner = IntentIntegrator(this)
            scanner.setCameraId(1)
            scanner.initiateScan()
            scanner.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
            scanner.setBeepEnabled(false)
            scanner.initiateScan()

        }

        val userid=findViewById<Button>(R.id.button6)
        userid.setOnClickListener {
            val intent6= Intent(this, EnteruseridActivity:: class.java)
            startActivity(intent6)
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

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (resultCode == RESULT_OK) {
            val result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
            if (result != null) {
                if (result.contents == null) {
                    Toast.makeText(this, "Cancelled", Toast.LENGTH_LONG).show()
                } else {
                    val uid = result.contents
                    val queue = Volley.newRequestQueue(this)
                    val url = "http://$myip/?cmd=VALIDATEUID&uid=$uid"
                    val req = JsonObjectRequest(Request.Method.GET, url,null, Response.Listener
                    {
                        val intent4= Intent(this,DisplayrActivity :: class.java)
                        startActivity(intent4)
                    }, Response.ErrorListener { error ->

                        Toast.makeText(applicationContext, error.message, Toast.LENGTH_SHORT).show()  })

                    queue.add(req)

                }
            } else {
                super.onActivityResult(requestCode, resultCode, data)
            }
        }
    }

    override fun onBackPressed() {

    }
}