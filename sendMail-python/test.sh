curl -d '{"imageName": "sample.jpg",   "recipient": "jonggyoukim@gmail.com", "imageSize" : "3x3" }' -H  "Content-Type: application/json" -X POST https://i5gj5hiysktuo443rlry6cyjii.apigateway.ap-seoul-1.oci.customer-oci.com/meetup/sendmail

echo '{"imageName": "sample.jpg",   "recipient": "jonggyoukim@gmail.com", "imageSize" : "3x3" }' | python3 sendmail.py
