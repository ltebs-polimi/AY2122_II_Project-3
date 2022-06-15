/* ========================================
 *
 *
 * ========================================
*/

// Include required header files
#include "project.h"
#include "MPU9250.h"
#include "buttonled.h"
#include "stdio.h"

#define N_FRAME 10
int flag_data_ready = 0; 
int i;
int k;
uint8_t packet_to_send[(N_FRAME*12)+2]; // 1 packet of data to send 
uint8_t data[12]; //1 frame of data read from the IMU

CY_ISR_PROTO(MPU9250_DR_ISR);

int main(void)
{
    // Enable glogal interrupts
    CyGlobalIntEnable; 
    
    // Start UART & BT components
    UART_Debug_Start();
    UART_BT_Start();
    
    UART_Debug_PutString("**************\r\n");
    UART_Debug_PutString("    MPU9250   \r\n");
    UART_Debug_PutString("**************\r\n");
//    UART_BT_PutString("**************\r\n");
//    UART_BT_PutString("    MPU9250   \r\n");
//    UART_BT_PutString("**************\r\n");
    
    // Start I2C component
    I2C_MPU9250_Master_Start();
    
    CyDelay(1000);
    
    char message[30];                       // Message to send over UART
    uint8_t connection = 0;                 // Variable to store connection status
    packet_to_send[(N_FRAME*12)+1] = 0xC0;  // tail
    packet_to_send[0] = 0xA0;               // header
    
    // Scan I2C bus and find devices
    for (int address = 0; address < 128; address++) {
        if (I2C_MPU9250_Master_MasterSendStart(address, 0) == I2C_MPU9250_Master_MSTR_NO_ERROR) {
            sprintf(message, "Found device at: 0x%02x\r\n", address);
            UART_Debug_PutString(message);
//            UART_BT_PutString(message);
        }
        I2C_MPU9250_Master_MasterSendStop();
    }
    
    // Wait until MPU9250 is connected
    do {
        connection = MPU9250_IsConnected();
    } while (connection == 0);
    
    // Show connection status feedback
    // PIN_LED_Write(1);
    
    // Star the MPU9250
    MPU9250_Start(); 


    // Read WHO AM I register and compare with the expected value
    uint8_t whoami = MPU9250_ReadWhoAmI();
    sprintf(message, "WHO AM I: 0x%02x - Expected: 0x%02x\r\n", whoami, MPU9250_WHO_AM_I);
    UART_Debug_PutString(message);
//    UART_BT_PutString(message);
    
   
    
    MPU9250_ISR_StartEx(MPU9250_DR_ISR);
    
    for(;;)
    {
        // Check for switch button
        //Button_pushed();
        
    }
}


CY_ISR(MPU9250_DR_ISR) { 
    
    PIN_LED_Write(1);
    // Load data on the packet to be sent
    for (i=0; i<N_FRAME; i++) {
        
        // Read data 
        MPU9250_ReadAccGyroRaw(&data[0]);
        
        for (k = (1+i*12); (k < (13+(i*12))); k++) {            
            packet_to_send[k] = data[(k-1)-(i*12)];     
            
        }
    }
            
    if (i == (N_FRAME)) {
        
        // Send packet over BT -> once having put inside the packet N_FRAME of data
//        UART_Debug_PutArray(packet_to_send,(N_FRAME*12)+2); 
        UART_BT_PutArray(packet_to_send,(N_FRAME*12)+2); 
        // Refresh the packet
        k = 0;
        i = 0;
        
    }
    
    MPU9250_ReadInterruptStatus();
    
}

/* [] END OF FILE */
