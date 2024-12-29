#include "MPU9250_WE.h"
#include <Wire.h>
#define MPU9250_ADDR 0x68

MPU9250_WE myMPU9250 = MPU9250_WE(MPU9250_ADDR);
float g = 0,b = 0,a = 0;//gamma, beta and alpha 
float wg = 0,wb = 0,wa = 0;//angular velocity (global frame)
float p = 0,q = 0,r = 0;//angular velocity (local frame)
float dt,t_ref = 0;
unsigned long count = 0;
void setup() {
  Serial.begin(9600);
  Wire.begin();
  if(!myMPU9250.init()){
    //Serial.println("MPU9250 does not respond");
  }
  else{
    //Serial.println("MPU9250 is connected");
  }
  if(!myMPU9250.initMagnetometer()){
    //Serial.println("Magnetometer does not respond");
  }
  else{
    //Serial.println("Magnetometer is connected");
  }

  //Serial.println("Position you MPU9250 flat and don't move it - calibrating...");
  delay(1000);
  myMPU9250.autoOffsets();
  //Serial.println("Done!");
  myMPU9250.enableGyrDLPF();
  
  myMPU9250.setGyrDLPF(MPU9250_DLPF_6);

  myMPU9250.setSampleRateDivider(5);

  myMPU9250.setGyrRange(MPU9250_GYRO_RANGE_250);

  myMPU9250.setAccRange(MPU9250_ACC_RANGE_2G);

  myMPU9250.enableAccDLPF(true);

  myMPU9250.setAccDLPF(MPU9250_DLPF_6);

  myMPU9250.setMagOpMode(AK8963_CONT_MODE_100HZ);
  delay(200);
}

void loop() {
  
  xyzFloat gyr = myMPU9250.getGyrValues();
 /* float M[3][3] = {{1,sin(g)*cos(b),cos(g)*tan(b)},
                   {0,   cos(g)    ,-sin(g)},
                   {0,sin(g)/cos(b),cos(g)/cos(b)}};*/
  float sa = sin(a);
  float ca = cos(a);
  float sb = sin(b);
  float cb = cos(b);
  float sg = sin(g);
  float cg = cos(g);                 
  float M[3][3] = {{ca*cb,ca*sb*sg - sa*cg,ca*sb*cg + sa*sg},
                   {sa*cb,sa*sb*sg + ca*cg,sa*sb*cg - ca*sg},
                   {-sb  ,cb*sg          ,cb*cg}};
  p = gyr.x*PI/180;
  q = gyr.y*PI/180;
  r = gyr.z*PI/180;
  wg = M[0][0]*p + M[0][1]*q + M[0][2]*r; 
  wb = M[1][0]*p + M[1][1]*q + M[1][2]*r;
  wa = M[2][0]*p + M[2][1]*q + M[2][2]*r;
  dt = (millis() - t_ref)/1000.0;
  g = g + dt*wg;
  b = b + dt*wb;
  a = a + dt*wa;
  count++;
  if(count%25==0){
    Serial.print(g);
    Serial.print(':');
    Serial.print(b);
    Serial.print(':');
    Serial.println(a);
  }
  t_ref = millis();
  //delay(10);
}
