package com.bas3d.asrs1

import android.content.Intent
import android.os.Bundle
import android.telephony.SmsManager
import android.text.TextUtils
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

class SmsActivity : AppCompatActivity(){
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sms)
        val send = findViewById<Button>(R.id.button10)
        val edittext=findViewById<EditText>(R.id.editText2)
        val textview=findViewById<TextView>(R.id.textView4)
        val queue = Volley.newRequestQueue(this)
        val url = "http://$myip/?cmd=GETUID"
        val stringRequest = StringRequest(Request.Method.GET, url, Response.Listener<String>
        {response ->

            textview.text=response

        }, Response.ErrorListener {

            Toast.makeText(applicationContext,"Error in getting user id", Toast.LENGTH_SHORT).show()  })
        queue.add(stringRequest)

        send.setOnClickListener {
            sendSMS((edittext.text.toString()), (textview.text).toString())
        }

        val exit=findViewById<ImageView>(R.id.imageView15)
        exit.setOnClickListener {
            exit.alpha=0.5f
            val queue1 = Volley.newRequestQueue(this)
            val url1 = "http://$myip/?cmd=AUTOHOME"
            val req = JsonObjectRequest(Request.Method.GET, url1,null, Response.Listener
            {

                val intent= Intent(this,HomeActivity::class.java)
                startActivity(intent)

            }, Response.ErrorListener { error ->
                Toast.makeText(applicationContext, error.message, Toast.LENGTH_SHORT).show()  })
            req.retryPolicy = DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)

            queue1.add(req)
        }
    }
    private fun sendSMS(phoneNo: String, msg: String) {

        if(TextUtils.isEmpty(phoneNo) || phoneNo.length!=10){
            Toast.makeText(applicationContext, "Enter phone number", Toast.LENGTH_SHORT).show()
            run {

            }
        }
        else {
            try {
                val smsManager = SmsManager.getDefault()
                smsManager.sendTextMessage(phoneNo, null, "Welcome to ASRS. Your ID is $msg Save the user ID for retrieval", null, null)
                Toast.makeText(applicationContext, "Message Sent", Toast.LENGTH_LONG).show()
                val i1 = Intent(this, ThankuActivity::class.java)
                startActivity(i1)

            } catch (ex: Exception) {
                Toast.makeText(applicationContext, ex.message.toString(), Toast.LENGTH_LONG).show()
                ex.printStackTrace()
            }
        }
    }


    override fun onBackPressed() {

    }
}