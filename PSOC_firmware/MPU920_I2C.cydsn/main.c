/* ========================================
 * Project 3 
 * FIRMWARE CODE - MPU9250 IMU SENSOR 
 * 
 * ========================================
*/


// Include required header files
#include "project.h"
#include "MPU9250.h"
#include "buttonled.h"
#include "stdio.h"

// Variables declaration
#define N_FRAME 10 
int flag_data_ready = 0; 
int i;
int k;
uint8_t packet_to_send[(N_FRAME*12)+2]; // 1 packet of data to send contains: N_FRAMES of data + header and tail
uint8_t data[12];                       // 1 frame of data read from the IMU


CY_ISR_PROTO(MPU9250_DR_ISR);

int main(void)
{
    // Enable global interrupt
    CyGlobalIntEnable; 
    
    // Start UART & BT components
    UART_Debug_Start();
    UART_BT_Start();
    
    // Start I2C component
    I2C_MPU9250_Master_Start();
    
    CyDelay(1000);
    
    uint8_t connection = 0;                 // variable to store connection status
    packet_to_send[(N_FRAME*12)+1] = 0xC0;  // tail
    packet_to_send[0] = 0xA0;               // header
    
    // Wait until MPU9250 is connected
    do {
        connection = MPU9250_IsConnected();
    } while (connection == 0);
    
    // Start the MPU9250
    MPU9250_Start(); 
    MPU9250_ISR_StartEx(MPU9250_DR_ISR);
    
    for(;;)
    {
        // Check for switch button
    }
}


CY_ISR(MPU9250_DR_ISR) {  
    
    PIN_LED_Write(1); // Always on for the user 
    
    // Load data on the packet to be sent
    for (i=0; i<N_FRAME; i++) {
        
        // Read data 
        MPU9250_ReadAccGyroRaw(&data[0]);
        
        for (k = (1+i*12); (k < (13+(i*12))); k++) {            
            packet_to_send[k] = data[(k-1)-(i*12)];      
        }
    }
            
    if (i == (N_FRAME)) {
        
        // Send packet over BT once having put inside the packet N_FRAME of data 
        UART_BT_PutArray(packet_to_send,(N_FRAME*12)+2); 
        
        // Refresh the packet
        k = 0;
        i = 0; 
    }
    
    MPU9250_ReadInterruptStatus();
    
}

/* [] END OF FILE */
