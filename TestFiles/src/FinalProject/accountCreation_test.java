package FinalProject;

import static org.junit.Assert.assertEquals;

import java.util.concurrent.TimeUnit;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class accountCreation_test {

	static WebDriver driver;

//	Change your selenium driver path here
	static String pathChromeDriver="C://COM_S_319/Lab_6/chromedriver.exe";
	static String pathLoginPage="file:///C:/COM_S_319/Final_Project/go-sports/HTML_Files/Create_Account.html";

	String name="name";
	String email="email";
	String psw="psw";
	String pswRepeat="pswRepeat";
	String RegisterButton="RegisterButton";
	String FinalResult="FinalResult";

	@BeforeClass
	public static void openBrowser()
	{
		System.setProperty("webdriver.chrome.driver", pathChromeDriver);
		driver= new ChromeDriver() ;
		driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
	}

	@AfterClass
	public static void closeBrowser() {
		driver.quit();
	}

	@Test
	public void passwordsFailedTest() throws InterruptedException {
		driver.get(pathLoginPage);
		driver.manage().window().maximize();
		driver.findElement(By.xpath("//input[@id='"+name+"']")).sendKeys("Kyle");
		driver.findElement(By.xpath("//input[@id='"+email+"']")).sendKeys("kjrooney@iastate.edu");
		driver.findElement(By.xpath("//input[@id='"+psw+"']")).sendKeys("BAD");
		driver.findElement(By.xpath("//input[@id='"+pswRepeat+"']")).sendKeys("Password123");

		Thread.sleep(1000);
		driver.findElement(By.id(RegisterButton)).click();
		Thread.sleep(3000);

		String strMessage = driver.findElement(By.id(FinalResult)).getText();
		assertEquals("Failed test case", strMessage, "Passwords do not match, please try again.");
		Thread.sleep(1000);
	}

	@Test
	public void emailFailedTest() throws InterruptedException {
		driver.get(pathLoginPage);
		driver.manage().window().maximize();
		driver.findElement(By.xpath("//input[@id='"+name+"']")).sendKeys("Kyle");
		driver.findElement(By.xpath("//input[@id='"+email+"']")).sendKeys("This will break");
		driver.findElement(By.xpath("//input[@id='"+psw+"']")).sendKeys("Password123");
		driver.findElement(By.xpath("//input[@id='"+pswRepeat+"']")).sendKeys("Password123");
		
		Thread.sleep(1000);
		driver.findElement(By.id(RegisterButton)).click();
		Thread.sleep(3000);
		
		String strMessage = driver.findElement(By.id(FinalResult)).getText();
		assertEquals("Failed test case", strMessage, "Email should be in form xxx@xxx.xxx, where x is alphanumeric!");
		Thread.sleep(1000);
	}
}
