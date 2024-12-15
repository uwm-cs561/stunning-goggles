import os
from unsloth import FastLanguageModel
from train import SAVED_WEIGHTS_DIR, max_seq_length, get_relative_path
from dataloader import CHAT_TEMPLATE


def inference(use_pretrained=False):
    model_path = os.path.join(SAVED_WEIGHTS_DIR, "trained_model-2024-12-02-08-49-29")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=(
            "unsloth/Llama-3.2-3B-Instruct-bnb-4bit" if use_pretrained else model_path
        ),
        max_seq_length=max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )
    FastLanguageModel.for_inference(model)  # Enable native 2x faster inference

    if False:
        model.save_pretrained_gguf(
            "model",
            tokenizer,
        )
    if False:
        model.save_pretrained_gguf("model", tokenizer, quantization_method="q4_k_m")
    # oom....

    messages = [
        {
            "role": "user",
            "content": """
            [INFO] Not compiling main sources
[INFO]
[INFO] --- maven-resources-plugin:2.6:testResources (default-testResources) @ testng-test ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Copying 77 resources
[INFO]
[INFO] --- maven-compiler-plugin:3.1:testCompile (default-testCompile) @ testng-test ---
[INFO] Nothing to compile - all classes are up to date
[INFO]
[INFO] --- maven-surefire-plugin:2.14.1:test (default-test) @ testng-test ---
[INFO] Surefire report directory: /home/travis/build/cbeust/testng/target/surefire-reports
-------------------------------------------------------
T E S T S
-------------------------------------------------------
Running TestSuite
[SimpleBaseTest] Warning: System property test.resources.dir was not defined.
[TestNG] [WARN] MethodInterceptor already set
Tests run: 617, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 24.321 sec <<< FAILURE!
compareFiles(test.yaml.YamlTest)  Time elapsed: 0.034 sec  <<< FAILURE!
java.lang.AssertionError: Lists differ at element [0]: [Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7] != [Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7] expected [[Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7]] but found [[Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7]]
at org.testng.Assert.fail(Assert.java:94)
at org.testng.Assert.failNotEquals(Assert.java:496)
at org.testng.Assert.assertEquals(Assert.java:125)
at org.testng.Assert.assertEquals(Assert.java:551)
at org.testng.Assert.assertEquals(Assert.java:516)
at test.yaml.YamlTest.compareFiles(YamlTest.java:38)
Results :
Failed tests:
YamlTest.compareFiles:38 Lists differ at element [0]: [Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7] != [Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7] expected [[Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7]] but found [[Suite: "SingleSuite"   [Test: "Test3" verbose:1[parameters:n=>43z=>foo][metagroups:a=b,d,] [included: A B ][excluded: CD]  classes: packages:org.testng.xml.XmlPackage@d9799c4d org.testng.xml.XmlPackage@d9799c6c ]    [Test: "Test1" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.A] [XmlClass class=test.tmp.B]  packages:]    [Test: "Test2" verbose:1[parameters:][metagroups:] [included: ][excluded: ]  classes:[XmlClass class=test.tmp.B]  packages:]   methodSelector:org.testng.xml.XmlMethodSelector@de9d8ee3 methodSelector:org.testng.xml.XmlMethodSelector@3715d9c7]]
Tests run: 617, Failures: 1, Errors: 0, Skipped: 0
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 28.023 s
[INFO] Finished at: 2015-05-08T00:33:38+00:00
[INFO] Final Memory: 12M/451M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.14.1:test (default-test) on project testng-test: There are test failures.
[ERROR]
[ERROR] Please refer to /home/travis/build/cbeust/testng/target/surefire-reports for the individual test results.
[ERROR] -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
travis_time:end:096f57ae:start=1431045189180531908,finish=1431045218800786465,duration=29620254557
[31;1mThe command "mvn -f pom-test.xml test -B" exited with 1.[0m
Done. Your build exited with 1.
""",
        },
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        # chat_template=CHAT_TEMPLATE,
        return_tensors="pt",
    ).to("cuda")

    from transformers import TextStreamer

    text_streamer = TextStreamer(tokenizer, skip_prompt=True)
    _ = model.generate(
        input_ids,
        streamer=text_streamer,
        max_new_tokens=max_seq_length,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=input_ids.ne(tokenizer.pad_token_id),
    )


if __name__ == "__main__":
    print("\n\nInference with fine-tuning")
    inference(False)

    print("\n\nInference without fine-tuning")
    inference(True)
