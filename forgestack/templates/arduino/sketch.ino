void setup() {
  Serial.begin(9600);
  Serial.println("ForgeStack Arduino bridge scaffold ready");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    Serial.print("echo: ");
    Serial.println(input);
  }
}