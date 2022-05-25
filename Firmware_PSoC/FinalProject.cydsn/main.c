/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/


// Include required header files
#include "project.h"
#include "MPU9250.h"
#include "MPU9250_RegMap.h"
#include "MPU9250_I2C.h"
#include "buttonled.h"
#include "stdio.h"

//Variables' declaration
#ifndef INT_FIFO_OFLOW_BIT
#define INT_FIFO_OFLOW_BIT 0x10
#endif


int int_status;
int packet_count;
int fifoCount;
int i;
int k;
int j;
uint8_t data[12];
int flag_send;
uint8_t data_to_send[434];
char message[30];       // Message to send over UART
uint8_t connection = 0; // Variable to store connection status


CY_ISR_PROTO(MPU9250_DR_ISR);

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */
    
    data_to_send[0] = 0xA0; //header
    data_to_send[433] = 0xC0; //tail

    // Start UART component
    UART_Debug_Start();
    
    UART_Debug_PutString("**************\r\n");
    UART_Debug_PutString("    MPU9250   \r\n");
    UART_Debug_PutString("**************\r\n");
    
    //Start BT component
    UART_BT_Start();
    
    // Start I2C component
    I2C_MPU9250_Master_Start();
    
    CyDelay(1000); //1 sec
   
    UART_BT_PutString("funziona");
    
    
    // Scan I2C bus and find devices
    for (int address = 0; address < 128; address++) {
        if (I2C_MPU9250_Master_MasterSendStart(address, 0) == I2C_MPU9250_Master_MSTR_NO_ERROR) {
            sprintf(message, "Found device at: 0x%02x\r\n", address);
            UART_Debug_PutString(message);
        }
        else {
            sprintf(message, "Not found on port : %d \r\n", address);
            UART_Debug_PutString(message);
        }
        I2C_MPU9250_Master_MasterSendStop();
    }
    
    // Wait until MPU9250 is connected
    do {
        connection = MPU9250_IsConnected();
    } while (connection == 0);
    
    // Start the MPU9250 with default values
    MPU9250_Start();
    
    // Set up accelerometer full scale range
    MPU9250_SetAccFS(MPU9250_Acc_FS_2g);
    // Set up gyroscope full scale range
    MPU9250_SetGyroFS(MPU9250_Gyro_FS_250);
    
    // Set up sample rate divider
    MPU9250_SetSampleRateDivider(4); // From 1kHz to 200 Hz sampling
    
    // Set up gyroscope digital low pass filter
    MPU9250_I2C_Write(MPU9250_I2C_ADDRESS, MPU9250_CONFIG_REG, 0x03);
    // Set up accelerometer digital low pass filter
    MPU9250_I2C_Write(MPU9250_I2C_ADDRESS, MPU9250_ACCEL_CONFIG_2_REG, 0x03);
    
    // Enable FIFO interrupt
    MPU9250_EnableFifoOverflowInterrupt();
    
    //Set up FIFO mode 
    MPU9250_EnableFifoOperationMode();
    MPU9250_ConfigFifoMode();
    MPU9250_WriteAccTempGyroDataToFIFO();
    

    for(;;)
    {   
        
        //Check for switch button
        Button_pushed();
        
        // Read number of bytes inside the buffer
        fifoCount = MPU9250_ReadBytesInFifoBuffer();
            
        // Check for fifo buffer overflow
        int_status = MPU9250_ReadInterruptStatus();
        if (int_status == INT_FIFO_OFLOW_BIT) {
        sprintf(message, "Overflow! fifoCount is: %d\r\n", fifoCount);
        PIN_LED_Write(1);
        UART_Debug_PutString(message);   
        }
        
        
        // First packet of information 
        if (fifoCount >=14) { //0-512

            // 1 packet of information is made of 14 bytes: 6 for acc, 2 for temp, 6 for gyro
            packet_count = (fifoCount/14);
            
            if (packet_count >= 36) { //maximum number of packets inside the fifo buffer (512 bytes in total -> 512/14 = 36)
                packet_count = 36;
                flag_send = 1; //the data collected can be sent via BT
                }
            
            for (i=0; i<packet_count;i++) { 
                                
                // Read data via I2C
                MPU9250_ReadAccGyroRaw(data); //data = array of 12 bytes: 6 for acc and 6 for gyro
                
                // Put the data into the array to send via BT                
                for (k=(1+i*12);(k<(13+(i*12)));k++) { 
                    data_to_send[k] = data[k-1]; //data_to_send = array of 432 bytes of data (36*12) + 2 for header and tail

                }
            }   
            
            // Send data via BT
            if (flag_send) {
                flag_send = 0;
//                UART_Debug_PutArray(data_to_send, 255);
                UART_BT_PutArray(data_to_send, 255);                  
            }
        }       
    }  
}



/* [] END OF FILE */
