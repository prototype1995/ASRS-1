package com.bas3d.asrs1

import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Bundle
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_capture.*
import org.json.JSONException
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.util.*

class CaptureActivity : AppCompatActivity() {

    private val CAMERA_REQUEST = 1888
    private val MY_CAMERA_PERMISSION_CODE = 100
    val myip=Global().ip

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_capture)
        val photoButton = findViewById<Button>(R.id.button15)
        photoButton.setOnClickListener {

            val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            cameraIntent.putExtra("android.intent.extras.CAMERA_FACING", 1)
            startActivityForResult(cameraIntent, CAMERA_REQUEST)
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == MY_CAMERA_PERMISSION_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "camera permission granted", Toast.LENGTH_LONG).show()
                val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                startActivityForResult(cameraIntent, CAMERA_REQUEST)
            } else {
                Toast.makeText(this, "camera permission denied", Toast.LENGTH_LONG).show()
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == CAMERA_REQUEST && resultCode == Activity.RESULT_OK) {
            val extras = data?.getExtras()
            val photo = extras?.get("data") as Bitmap
            imageView14.setImageBitmap(photo)
            val image = getStringImage(photo)
            val button = findViewById<Button>(R.id.button16)
            button.setOnClickListener {
                sendImage(image)
                val intent=Intent(this,PrintActivity::class.java)
                startActivity(intent)
            }
        }
    }

    private fun getStringImage(photo: Bitmap): String? {

        val baos = ByteArrayOutputStream()
        photo.compress(Bitmap.CompressFormat.JPEG, 100, baos)
        val imageBytes = baos.toByteArray()
        val encodeImage = Base64.encodeToString(imageBytes, Base64.DEFAULT)
        return encodeImage

    }

    private fun sendImage(image: String?) {

        val que= Volley.newRequestQueue(this)
        val url="http://$myip/?cmd=UPLOADIMAGE"
        val stringRequest = object:StringRequest(Method.POST, url, Response.Listener<String>
        { response ->

            Log.i("Myresponse",""+response)
            Toast.makeText(this, ""+response, Toast.LENGTH_SHORT).show()

        }, Response.ErrorListener {

            Toast.makeText(this, "No internet connection", Toast.LENGTH_LONG).show()
        }){

            override fun getParams(): Map<String, String> {
                val params = Hashtable<String, String>()
                params.put("image", image)
                return params

            }
        }

        que.add(stringRequest)
    }

}